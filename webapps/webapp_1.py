# Import javascript modules
from js import THREE, window, document, Object, console
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
    
    # Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(1,1,1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.x = 100
    camera.position.y = 50
    camera.position.z = -25
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 

    # Define colors
    primary_color = THREE.Color.new(0.1,0.45,0.8)
    secondary_color = THREE.Color.new(1,0,0)

    # Create material
    global material
    material = THREE.MeshBasicMaterial.new()
    material.color = primary_color
    material.transparent = True
    material.opacity = 0.5

    # Create line material 
    global line_material
    line_material = THREE.LineBasicMaterial.new()
    line_material.color = primary_color

    # Create floor material
    global floor_material
    floor_material = THREE.MeshBasicMaterial.new()
    floor_material.color = secondary_color
    floor_material.transparent = True
    floor_material.opacity = 0.35

    # Create floor line material
    global floor_line_material
    floor_line_material = THREE.LineBasicMaterial.new()
    floor_line_material.color = secondary_color

    # Declare update lists
    global geometry_list, line_geometry_list
    geometry_list =  []
    line_geometry_list = []

    # Set up GUI
    # Step 1
    global params_1, stair_height
    stair_height = 350

    params_1 = {
            'Treppenhöhe': stair_height
    }
    params_1 = Object.fromEntries(to_js(params_1))

    # Step 2
    global params_2, step_number, step_height, step_depth
    step_number = 20
    step_height = 17.5
    step_depth = 28

    params_2 = {
            'Stufenanzahl': step_number,
            'Stufenhöhe': step_height,
            'Stufenauftritt': step_depth
    }
    params_2 = Object.fromEntries(to_js(params_2))

    # Step 3
    global params_3, landing_position, landing_size, stair_lenght
    landing_position = 10
    landing_size = 2
    stair_lenght = 658

    params_3 = {
            
            'Podestposition': landing_position,
            'Podestgröße': landing_size,
            'Treppenlänge': stair_lenght
    }
    params_3 = Object.fromEntries(to_js(params_3))

    # Step 4
    global params_4, step_width
    step_width = 125

    params_4 = {
            'Stufenbreite': step_width,
    }
    params_4 = Object.fromEntries(to_js(params_4))

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    global gui, param1, param2, param3, param4, param5, param6, param7, param8
    gui = window.dat.GUI.new()
    
    # Step 1
    param_folder1 = gui.addFolder('1. Treppenhöhe')
    param1 = param_folder1.add(params_1, 'Treppenhöhe', 21,500,1)
    param_folder1.open()

    # Step 2
    param_folder2 = gui.addFolder('2. Stufenanzahl')
    param2 = param_folder2.add(params_2, 'Stufenanzahl', 1,33,1)
    param3 = param_folder2.add(params_2, 'Stufenhöhe', 15,21,0.1)
    param4 = param_folder2.add(params_2, 'Stufenauftritt', 21,33,0.1)
    param_folder2.open()

    # Step 3
    param_folder3 = gui.addFolder('3. Treppenlänge')
    param5 = param_folder3.add(params_3, 'Podestposition', 5,18,1)
    param6 = param_folder3.add(params_3, 'Podestgröße', 1,3,1)
    param7 = param_folder3.add(params_3, 'Treppenlänge', 21,2190,1)
    param_folder3.open()

    # Step 4
    param_folder4 = gui.addFolder('4. Treppenbreite')
    param8 = param_folder4.add(params_4, 'Stufenbreite', 80,250,1)
    param_folder1.open()
    
    #-----------------------------------------------------------------------
    # Inital_stair
    construct_stair(step_width, step_height, step_depth, step_number, landing_position, landing_size)
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Construct Stairs
def construct_stair(width, height, depth, number, position, size):
    # Scale, Shift
    s = 10
    shift = 0

    for step in geometry_list:
        scene.remove(step)

    for line in line_geometry_list:
        scene.remove(line)

    # Floors
    floor_geometry = THREE.BoxGeometry.new(50,3,20)

    # Lower floor
    lower_floor = THREE.Mesh.new(floor_geometry, floor_material)

    lower_floor_geometry_line = THREE.EdgesGeometry.new(lower_floor.geometry)
    lower_floor_lines = THREE.LineSegments.new(lower_floor_geometry_line, floor_line_material)

    lower_floor.position.set(0, -0.5*3 -0.5*height/s,-20*0.5 - depth*step_number*0.5/s - depth*0.5/s)
    lower_floor_lines.position.set(0, -0.5*3 -0.5*height/s,-20*0.5 - depth*step_number*0.5/s - depth*0.5/s)

    scene.add(lower_floor)
    geometry_list.append(lower_floor)
    scene.add(lower_floor_lines)
    line_geometry_list.append(lower_floor_lines)

    # Upper floor
    upper_floor = THREE.Mesh.new(floor_geometry, floor_material)

    upper_floor_geometry_line = THREE.EdgesGeometry.new(upper_floor.geometry)
    upper_floor_lines = THREE.LineSegments.new(upper_floor_geometry_line, floor_line_material)

    upper_floor.position.set(0,step_height*step_number/s - 0.5*3 - 0.5*height/s, 20*0.5 - depth*step_number*0.5/s - depth*0.5/s + (step_number-1)*step_depth/s + math.floor((step_number-1)/landing_position)*63*size/s)
    upper_floor_lines.position.set(0,step_height*step_number/s - 0.5*3 - 0.5*height/s, 20*0.5 - depth*step_number*0.5/s - depth*0.5/s + (step_number-1)*step_depth/s + math.floor((step_number-1)/landing_position)*63*size/s)

    scene.add(upper_floor)
    geometry_list.append(upper_floor)
    scene.add(upper_floor_lines)
    line_geometry_list.append(upper_floor_lines)
    
    # Geometries
    step_geometry = THREE.BoxGeometry.new(width/s, height/s, depth/s)
    landing_geometry = THREE.BoxGeometry.new(width/s, height/s, (depth + 63*size)/s)

    for i in range(number - 1):
        # Landing
        if (i + 1) % position == 0:
            shift += 1

            landing = THREE.Mesh.new(landing_geometry, material)

            landing_geometry_line = THREE.EdgesGeometry.new(landing.geometry)
            landing_lines = THREE.LineSegments.new(landing_geometry_line, line_material)

            landing.position.set(0, height*i/s, depth*i/s - depth*step_number*0.5/s + shift*63*size*0.5/s + (shift-1)*63*size*0.5/s)
            landing_lines.position.set(0, height*i/s, depth*i/s - depth*step_number*0.5/s + shift*63*size*0.5/s + (shift-1)*63*size*0.5/s)
            
            scene.add(landing)
            geometry_list.append(landing)
            scene.add(landing_lines)
            line_geometry_list.append(landing_lines)

        # Step
        if (i + 1) % position != 0:
            step = THREE.Mesh.new(step_geometry, material)

            step_geometry_line = THREE.EdgesGeometry.new(step.geometry)
            step_lines = THREE.LineSegments.new(step_geometry_line, line_material)

            step.position.set(0, height*i/s, depth*i/s - depth*step_number*0.5/s + shift*63*size/s)
            step_lines.position.set(0, height*i/s, depth*i/s - depth*step_number*0.5/s + shift*63*size/s)

            scene.add(step)
            geometry_list.append(step)
            scene.add(step_lines)
            line_geometry_list.append(step_lines)

def update():
    global stair_height, step_number, step_height, step_depth, landing_position, landing_size, stair_lenght, step_width

    if params_1.Treppenhöhe != stair_height or params_2.Stufenanzahl != step_number:
        stair_height = params_1.Treppenhöhe 
        step_number = params_2.Stufenanzahl

        step_height = stair_height/step_number
        params_2.Stufenhöhe = step_height 
        param3.updateDisplay()

        step_depth = 63 - 2* step_height
        params_2.Stufenauftritt = step_depth 
        param4.updateDisplay()

        stair_lenght = (step_number-1) * step_depth + math.floor((step_number-1)/landing_position)*63*landing_size 
        params_3.Treppenlänge = stair_lenght
        param7.updateDisplay()
        
        construct_stair(step_width, step_height, step_depth, step_number, landing_position, landing_size)

    elif params_2.Stufenhöhe != step_height:
        step_height = params_2.Stufenhöhe

        step_number = math.floor(stair_height / step_height)
        params_2.Stufenanzahl = step_number 
        param2.updateDisplay()

        step_height = stair_height/step_number
        params_2.Stufenhöhe = step_height 
        param3.updateDisplay()

        step_depth = 63 - 2* step_height
        params_2.Stufenauftritt = step_depth 
        param4.updateDisplay()

        stair_lenght = (step_number-1) * step_depth + math.floor((step_number-1)/landing_position)*63*landing_size 
        params_3.Treppenlänge = stair_lenght
        param7.updateDisplay()
        
        construct_stair(step_width, step_height, step_depth, step_number, landing_position, landing_size)

    elif params_2.Stufenauftritt != step_depth:
        step_depth = params_2.Stufenauftritt

        step_height = (63 - step_depth)/2
        params_2.Stufenhöhe = step_height 
 
        step_number = math.floor(stair_height / step_height)
        params_2.Stufenanzahl = step_number 
        param2.updateDisplay()

        step_height = stair_height/step_number
        params_2.Stufenhöhe = step_height 
        param3.updateDisplay()

        step_depth = 63 - 2* step_height
        params_2.Stufenauftritt = step_depth 
        param4.updateDisplay()

        stair_lenght = (step_number-1) * step_depth + math.floor((step_number-1)/landing_position)*63*landing_size 
        params_3.Treppenlänge = stair_lenght
        param7.updateDisplay()
        
        construct_stair(step_width, step_height, step_depth, step_number, landing_position, landing_size)
    
    elif params_3.Podestposition != landing_position or params_3.Podestgröße != landing_size:
        landing_position = params_3.Podestposition
        landing_size = params_3.Podestgröße

        stair_lenght = (step_number-1) * step_depth + math.floor((step_number-1)/landing_position)*63*landing_size 
        params_3.Treppenlänge = stair_lenght
        param7.updateDisplay()

        construct_stair(step_width, step_height, step_depth, step_number, landing_position, landing_size)

    elif params_3.Treppenlänge != stair_lenght:
        stair_lenght = params_3.Treppenlänge

        step_depth = (stair_lenght - (math.floor((step_number-1)/landing_position)*63*landing_size)) / (step_number - 1)
        params_2.Stufenauftritt = step_depth 
        param4.updateDisplay()

        construct_stair(step_width, step_height, step_depth, step_number, landing_position, landing_size)

    elif params_4.Stufenbreite != step_width:
        step_width = params_4.Stufenbreite

        construct_stair(step_width, step_height, step_depth, step_number, landing_position, landing_size)

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update()
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