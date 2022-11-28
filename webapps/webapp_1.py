# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls,composer
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 50
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation

    # Parameters
    global geom1_params, cylinders, cylinder_edges, cylinders_spread, cylinder_edges_spread
    cylinders = []
    cylinder_edges = []
    cylinders_spread = []
    cylinder_edges_spread = []
    geom1_params = {"steps":25, "riser_height":1.5, "tread_width":15, "tread_depth":20, "spread":0}
    geom1_params = Object.fromEntries(to_js(geom1_params))
   
    #Materials
    global material
    cylinder_color = THREE.Color.new(255,255,255)
    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 0.5
    material.color = cylinder_color

    global line_material
    edge_color = THREE.Color.new(100, 100, 100)
    line_material = THREE.LineBasicMaterial.new()
    line_material.color = edge_color

    #Store GUI Parameters once
    global riser_heights, tread_widths, tread_depths, spread
    riser_heights = geom1_params.riser_height
    tread_widths = geom1_params.tread_width 
    tread_depths = geom1_params.tread_depth 
    spread = geom1_params.spread

    #Cylinder Creation
    for i in range(geom1_params.steps):
        geometry = THREE.CylinderGeometry.new(geom1_params.tread_width, geom1_params.tread_width, geom1_params.riser_height, 64, 1, False, 0, math.radians(geom1_params.tread_depth))
        geometry.rotateY(math.radians(geom1_params.tread_depth)*i)
        geometry.translate(0, geom1_params.riser_height*i, 0)

        cylinder = THREE.Mesh.new(geometry, material)
        scene.add(cylinder)
        cylinders.append(cylinder)
    
        geometry_edge = THREE.EdgesGeometry.new(cylinder.geometry)

        cylinder_edge = THREE.LineSegments.new(geometry_edge, line_material)
        scene.add(cylinder_edge)
        cylinder_edges.append(cylinder_edge)

        # Get direction in which step points
        direction = THREE.Vector3.new( 0, 0, geom1_params.tread_width)
        direction.applyAxisAngle(THREE.Vector3.new(0, 1, 0), math.radians(geom1_params.tread_depth)*i + math.radians(geom1_params.tread_depth)/2)

        for t in range(geom1_params.spread):
            geometry_spread = THREE.CylinderGeometry.new(geom1_params.tread_width, geom1_params.tread_width, geom1_params.riser_height, 64, 1, False, 0, math.radians(geom1_params.tread_depth))
            geometry_spread.rotateY(math.radians(geom1_params.tread_depth)*i)
            # neighbouring Stairways twist in opposite directions
            geometry_spread.translate(0, geom1_params.riser_height*i*-(-1)**t, 0)
            # Stairways are moved to the same level
            geometry_spread.translate (0, geom1_params.steps * geom1_params.riser_height * (((-1)**t + 1)/2), 0)
            geometry_spread.translate (direction.x*t + direction.x, direction.y*t + direction.y , direction.z*t + direction.z)

            cylinder_spread = THREE.Mesh.new(geometry_spread, material)
            scene.add(cylinder_spread)
            cylinders_spread.append(cylinder_spread)
    
            geometry_edge_spread = THREE.EdgesGeometry.new(cylinder_spread.geometry)

            cylinder_edge_spread = THREE.LineSegments.new(geometry_edge_spread, line_material)
            scene.add(cylinder_edge_spread)
            cylinder_edges_spread.append(cylinder_edge_spread)

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'steps', 1,100,1)
    param_folder.add(geom1_params, 'tread_depth', 5,45)
    param_folder.add(geom1_params, 'tread_width', 10,40,1)
    param_folder.add(geom1_params, 'riser_height', 1, 5, 0.1)
    param_folder.add(geom1_params, 'spread', 0, 10, 1)
    param_folder.open()
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Update Stairway
def update_cylinders():
    global material, line_material, cylinders, cylinder_edges, cylinders_spread, cylinder_edges_spread
    global riser_heights, tread_widths, tread_depths, spread
    # If number of steps is changed, all Stairways must be rebuild
    if len(cylinders) != 0:
        if len(cylinders) != geom1_params.steps:

            for cylinder in cylinders:
                scene.remove(cylinder)
            for cylinder_edge in cylinder_edges:
                scene.remove(cylinder_edge)
            for cylinder_spread in cylinders_spread:
                scene.remove(cylinder_spread)
            for cylinder_edge_spread in cylinder_edges_spread:
                scene.remove(cylinder_edge_spread)

            cylinders_spread = []
            cylinder_edges_spread = []
            cylinders = []
            cylinder_edges = []

            for i in range(geom1_params.steps):
                geometry = THREE.CylinderGeometry.new(geom1_params.tread_width, geom1_params.tread_width, geom1_params.riser_height, 64, 1, False, 0, math.radians(geom1_params.tread_depth))
                geometry.rotateY(math.radians(geom1_params.tread_depth)*i)
                geometry.translate(0, geom1_params.riser_height*i, 0)

                cylinder = THREE.Mesh.new(geometry, material)
                scene.add(cylinder)
                cylinders.append(cylinder)
    
                geometry_edge = THREE.EdgesGeometry.new(cylinder.geometry)

                cylinder_edge = THREE.LineSegments.new(geometry_edge,line_material)
                scene.add(cylinder_edge)
                cylinder_edges.append(cylinder_edge)    
                
                position = THREE.Vector3.new( 0, 0, geom1_params.tread_width)
                position.applyAxisAngle(THREE.Vector3.new(0, 1, 0), math.radians(geom1_params.tread_depth)*i + math.radians(geom1_params.tread_depth)/2)

                for t in range(geom1_params.spread): 
                    geometry_spread = THREE.CylinderGeometry.new(geom1_params.tread_width, geom1_params.tread_width, geom1_params.riser_height, 64, 1, False, 0, math.radians(geom1_params.tread_depth))
                    geometry_spread.rotateY(math.radians(geom1_params.tread_depth)*i)
                    geometry_spread.translate(0, geom1_params.riser_height*i*-(-1)**t, 0)
                    geometry_spread.translate (0, geom1_params.steps * geom1_params.riser_height * (((-1)**t + 1)/2), 0)
                    geometry_spread.translate (position.x*t + position.x, position.y*t + position.y , position.z*t + position.z)

                    cylinder_spread = THREE.Mesh.new(geometry_spread, material)
                    scene.add(cylinder_spread)
                    cylinders_spread.append(cylinder_spread)
    
                    geometry_edge_spread = THREE.EdgesGeometry.new(cylinder_spread.geometry)

                    cylinder_edge_spread = THREE.LineSegments.new(geometry_edge_spread, line_material)
                    scene.add(cylinder_edge_spread)
                    cylinder_edges_spread.append(cylinder_edge_spread)

        #If Paramters are changed
        if riser_heights != geom1_params.riser_height or tread_widths != geom1_params.tread_width or tread_depths != geom1_params.tread_depth or spread != geom1_params.spread:
            #Store new GUI Parameters
            riser_heights = geom1_params.riser_height
            tread_widths = geom1_params.tread_width 
            tread_depths = geom1_params.tread_depth 
            spread = geom1_params.spread

            for cylinder_spread in cylinders_spread:
                scene.remove(cylinder_spread)
            for cylinder_edge_spread in cylinder_edges_spread:
                scene.remove(cylinder_edge_spread)
            cylinders_spread = []
            cylinder_edges_spread = []

            for i in range(len(cylinders)):
                cylinder = cylinders[i]
                cylinder_edge = cylinder_edges[i]

                geometry = THREE.CylinderGeometry.new(geom1_params.tread_width, geom1_params.tread_width, geom1_params.riser_height, 64, 1, False, 0, math.radians(geom1_params.tread_depth))
                geometry.rotateY(math.radians(geom1_params.tread_depth)*i)
                geometry.translate(0, geom1_params.riser_height*i, 0)
                cylinder.geometry = geometry
    
                geometry_edge = THREE.EdgesGeometry.new(cylinder.geometry)
                cylinder_edge.geometry = geometry_edge

                position = THREE.Vector3.new( 0, 0, geom1_params.tread_width)
                position.applyAxisAngle(THREE.Vector3.new(0, 1, 0), math.radians(geom1_params.tread_depth)*i + math.radians(geom1_params.tread_depth)/2)

                for t in range(geom1_params.spread): 
                    geometry_spread = THREE.CylinderGeometry.new(geom1_params.tread_width, geom1_params.tread_width, geom1_params.riser_height, 64, 1, False, 0, math.radians(geom1_params.tread_depth))
                    geometry_spread.rotateY(math.radians(geom1_params.tread_depth)*i)
                    geometry_spread.translate(0, geom1_params.riser_height*i*-(-1)**t, 0)
                    geometry_spread.translate (0, geom1_params.steps * geom1_params.riser_height * (((-1)**t + 1)/2), 0)
                    geometry_spread.translate (position.x*t + position.x, position.y*t + position.y , position.z*t + position.z)

                    cylinder_spread = THREE.Mesh.new(geometry_spread, material)
                    scene.add(cylinder_spread)
                    cylinders_spread.append(cylinder_spread)
    
                    geometry_edge_spread = THREE.EdgesGeometry.new(cylinder_spread.geometry)

                    cylinder_edge_spread = THREE.LineSegments.new(geometry_edge_spread, line_material)
                    scene.add(cylinder_edge_spread)
                    cylinder_edges_spread.append(cylinder_edge_spread)    
        #If there are no changes at all            
        else: 
            pass
# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_cylinders()
    controls.update()
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()

#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()

