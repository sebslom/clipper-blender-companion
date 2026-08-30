import bpy
import gpu
import blf
import math
import time
import random
from gpu_extras.batch import batch_for_shader

bl_info = {
    "name": "Clipper Companion",
    "author": "Antigravity AI",
    "version": (1, 1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Clipper",
    "description": "An interactive 3D Viewport companion (Clipper) that gives modeling tips and interactive tutorials.",
    "category": "Interface",
}

# --- GLOBAL DATA ---
TIPS = {
    "EN": [
        "Tip: Press Shift + A to add new objects, meshes, lights, or cameras!",
        "Tip: Press Tab to quickly toggle between Object Mode and Edit Mode.",
        "Tip: G is for Grab (move), R is for Rotate, and S is for Scale.",
        "Tip: While moving (G), rotating (R), or scaling (S), press X, Y, or Z to lock to that axis!",
        "Tip: Use the middle mouse button (scroll click) to orbit your 3D Viewport.",
        "Tip: Hold Shift + Middle Mouse Button to pan your view around the viewport.",
        "Tip: Press NumPad 0 to toggle active camera view.",
        "Tip: Press NumPad 1 for Front view, NumPad 3 for Right view, and NumPad 7 for Top view!",
        "Tip: In Edit Mode, press 1, 2, or 3 to switch selection modes (Vertex, Edge, Face).",
        "Tip: Press Ctrl + Z to undo, and Ctrl + Shift + Z to redo your actions.",
        "Tip: Press F2 to rename the selected object instantly.",
        "Tip: Press Alt + G, Alt + R, or Alt + S to reset an object's position, rotation, or scale!",
        "Tip: Press Shift + D to duplicate selected objects.",
        "Tip: In Edit Mode, select a face and press E to extrude it.",
        "Tip: Press Ctrl + B in Edit Mode to bevel selected edges or vertices.",
        "Tip: Press Ctrl + R in Edit Mode to add loop cuts to your mesh.",
        "Tip: Press I in Edit Mode to inset the selected faces.",
        "Tip: Hold Z to open the shading pie menu and switch between Wireframe, Solid, and Rendered modes!",
        "Tip: Press H to hide selected objects, and Alt + H to unhide everything in the scene!",
        "Tip: Press Slash (/) on NumPad to isolate selected objects in Local View!",
        "Tip: Press Ctrl + J to join multiple selected objects into a single mesh.",
        "Tip: Press P in Edit Mode to separate selected faces into a new object.",
        "Tip: Press M in Object Mode to move selected objects into a new Collection.",
        "Tip: Press Shift + Spacebar to open the full screen interactive tool menu!",
        "Tip: Press F3 to open the quick operator search bar to find any command!",
        "Tip: In Shader Editor, press Ctrl + T (with Node Wrangler enabled) to add Mapping and Texture Coordinate nodes!",
        "Tip: Press Spacebar to play or pause your keyframe animation!",
        "Tip: In Sculpt Mode, press Shift + F to adjust brush strength, and F to adjust brush size.",
        "Tip: Hold Shift while dragging any slider in Blender to make precision fine-adjustments!",
        "Tip: Hover over any input field and press Ctrl + C to copy its value, and Ctrl + V to paste it!",
        # --- Advanced Tips (EN) ---
        "Tip: Press Shift + A in Geometry Nodes to search for nodes like Instance on Points or Set Position!",
        "Tip: Drag any attribute output directly to the Group Output node to expose it in the Modifier panel.",
        "Tip: Use the Simulation Zone in Geometry Nodes to build realtime solvers, fire, and particle interactions!",
        "Tip: Use the Repeat Zone in Geometry Nodes to easily iterate loops without chaining multiple nodes.",
        "Tip: Enable 'Shade Auto Smooth' and use Weighted Normal modifier for pristine CAD highlights!",
        "Tip: Hold Shift + V in Edit Mode to slide vertices along their connected edge constraints.",
        "Tip: Press K in Edit Mode for the Knife tool, press C to cut through entire geometry, and Z to constrain angles.",
        "Tip: Use Ctrl + Shift + B to bevel individual vertices instead of edges in Edit Mode.",
        "Tip: Select edge loops with Alt + Left Click for fast topology selection.",
        "Tip: Use Alt + E in Edit Mode for the Extrude menu (Extrude Along Normals, Extrude Individual Faces).",
        "Tip: Press Shift + N in Edit Mode to recalculate normals outwards if shading looks flipped or dark.",
        "Tip: In Cycles, set Noise Threshold under Sampling to speed up renders without sacrificing image quality.",
        "Tip: Use AgX color management under View Transform for realistic highlight roll-off and cinematic colors!",
        "Tip: Enable Denoising (OpenImageDenoise or OptiX) in Cycles render settings for clean images with fewer samples.",
        "Tip: Add a Ray Portal BSDF node in Cycles for seamless non-Euclidean portals and recursive reflections!",
        "Tip: Use Light Groups in Cycles to adjust individual light intensities post-render without re-rendering!",
        "Tip: Use Cryptomatte pass in Cycles to automatically create perfect selection masks for objects and materials!",
        "Tip: Enable Screen Space Reflections and Subsurface Scattering in EEVEE Next for photorealistic realtime materials.",
        "Tip: Press Shift + E in Graph Editor to extend curve extrapolation (Linear, Make Cyclic for looping).",
        "Tip: Right-click any property and choose Add Driver to link properties using Python math expressions!",
        "Tip: Add an Inverse Kinematics (IK) constraint to bone chains for effortless character leg and arm posing.",
        "Tip: Press Stash or Push Down in Dope Sheet to move keyframe actions into the NLA Editor for non-linear blending.",
        "Tip: Use Shape Keys in Object Data Properties to create morph targets and facial expressions.",
        "Tip: Press Ctrl + Tab in Viewport with an Armature selected to toggle Pose Mode instantly.",
        "Tip: Use Dyntopo (Dynamic Topology) in Sculpt Mode to automatically add detail geometry on the fly!",
        "Tip: Press Ctrl + R in Sculpt Mode to perform Voxel Remesh and rebuild clean uniform sculpt topology.",
        "Tip: Use Multiresolution modifier to sculpt high-poly details while preserving base low-poly mesh levels.",
        "Tip: Hold Shift in Sculpt Mode with any brush active to smoothly blend surface bumps.",
        "Tip: Use Face Sets (W menu) in Sculpt Mode to isolate and hide specific mesh areas while sculpting.",
        "Tip: Enable Depth of Field on Camera and select a focus object for dramatic cinematic focus blur.",
        "Tip: Change Lens Focal Length to 85mm or 135mm for flattering character portraits without perspective distortion.",
        "Tip: Turn on Composition Guides (Rule of Thirds, Golden Ratio) under Camera Viewport Display.",
        "Tip: Press Ctrl + B in Camera View to draw a Render Border box and render only a cropped viewport region!",
        "Tip: Press Ctrl + Alt + NumPad 0 to align active camera directly to your current viewport perspective.",
        "Tip: Use Alt + D to create Linked Duplicates—they share geometry data and save massive RAM!",
        "Tip: Use Collection Instances to replicate complex props thousands of times with zero performance penalty.",
        "Tip: Press Ctrl + L to link materials, modifiers, or animation data across multiple selected objects.",
        "Tip: Use the Decimate modifier to quickly reduce polygon counts on background asset meshes.",
        "Tip: Press Shift + C to snap the 3D Cursor to the world origin (0,0,0) and view all objects."
    ],
    "PL": [
        "Wskazówka: Naciśnij Shift + A, aby dodać nowe obiekty, siatki, światła lub kamery!",
        "Wskazówka: Naciśnij Tab, aby szybko przełączać się między Trybem Obiektowym a Trybem Edycji.",
        "Wskazówka: G służy do przesuwania (Grab), R do obracania (Rotate), a S do skalowania (Scale).",
        "Wskazówka: Podczas przesuwania (G), obracania (R) lub skalowania (S) naciśnij X, Y lub Z, aby zablokować oś!",
        "Wskazówka: Użyj środkowego przycisku myszy (rolki), aby obracać widok 3D.",
        "Wskazówka: Przytrzymaj Shift + Środkowy Przycisk Myszy, aby przesuwać widok w boki.",
        "Wskazówka: Naciśnij NumPad 0, aby włączyć lub wyłączyć widok z aktywnej kamery.",
        "Wskazówka: NumPad 1 to widok z przodu, NumPad 3 to widok z prawej, a NumPad 7 to widok z góry!",
        "Wskazówka: W Trybie Edycji naciśnij 1, 2 lub 3, aby zmienić tryb zaznaczania (Wierzchołki, Krawędzie, Ściany).",
        "Wskazówka: Naciśnij Ctrl + Z, aby cofnąć, oraz Ctrl + Shift + Z, aby ponowić działanie.",
        "Wskazówka: Naciśnij F2, aby natychmiast zmienić nazwę zaznaczonego obiektu.",
        "Wskazówka: Naciśnij Alt + G, Alt + R lub Alt + S, aby zresetować pozycję, obrót lub skalę obiektu!",
        "Wskazówka: Naciśnij Shift + D, aby powielić (zduplikować) zaznaczone obiekty.",
        "Wskazówka: W Trybie Edycji zaznacz ścianę i naciśnij E, aby ją wyciągnąć (wytłoczyć).",
        "Wskazówka: Naciśnij Ctrl + B w Trybie Edycji, aby sfazować krawędzie lub wierzchołki.",
        "Wskazówka: Naciśnij Ctrl + R w Trybie Edycji, aby dodać cięcia pętli (Loop Cut).",
        "Wskazówka: Naciśnij I w Trybie Edycji, aby wciąć zaznaczoną ścianę (Inset).",
        "Wskazówka: Przytrzymaj Z, aby otworzyć menu trybów cieniowania (Wireframe, Solid, Rendered)!",
        "Wskazówka: Naciśnij H, aby ukryć zaznaczone obiekty, oraz Alt + H, aby odkryć wszystko!",
        "Wskazówka: Naciśnij Slash (/) na NumPadzie, aby odizolować zaznaczony obiekt w Widoku Lokalnym!",
        "Wskazówka: Naciśnij Ctrl + J, aby połączyć kilka zaznaczonych obiektów w jedną siatkę.",
        "Wskazówka: Naciśnij P w Trybie Edycji, aby odseparować zaznaczone ściany do nowego obiektu.",
        "Wskazówka: Naciśnij M w Trybie Obiektowym, aby przenieść zaznaczone obiekty do nowej Kolekcji.",
        "Wskazówka: Naciśnij Shift + Spacebar, aby otworzyć pełnoekranowe menu narzędzi!",
        "Wskazówka: Naciśnij F3, aby otworzyć szybkie wyszukiwanie operacji i poleceń!",
        "Wskazówka: W Edytorze Shaderów naciśnij Ctrl + T (z Node Wrangler), aby dodać węzły tekstury!",
        "Wskazówka: Naciśnij Spację, aby odtworzyć lub wstrzymać animację!",
        "Wskazówka: W Trybie Rzeźbienia naciśnij Shift + F dla siły pędzla, oraz F dla rozmiaru.",
        "Wskazówka: Przytrzymaj Shift podczas przeciągania suwaka, aby precyzyjnie dostosować wartość!",
        "Wskazówka: Najedź na dowolne pole numeryczne i naciśnij Ctrl + C, aby skopiować, oraz Ctrl + V, aby wkleić!",
        # --- Zaawansowane Wskazówki (PL) ---
        "Wskazówka: Naciśnij Shift + A w Geometry Nodes, aby wyszukiwać węzły takie jak Instance on Points czy Set Position!",
        "Wskazówka: Przeciągnij dowolne wyjście atrybutu do węzła Group Output, aby edytować go w panelu Modyfikatorów.",
        "Wskazówka: Użyj strefy Simulation Zone w Geometry Nodes do tworzenia symulacji w czasie rzeczywistym!",
        "Wskazówka: Użyj strefy Repeat Zone w Geometry Nodes, aby łatwo pętlić i powtarzać operacje na węzłach.",
        "Wskazówka: Włącz 'Shade Auto Smooth' oraz dodaj modyfikator Weighted Normal dla idealnych odblasków CAD!",
        "Wskazówka: Przytrzymaj Shift + V w Trybie Edycji, aby przesuwać wierzchołki wzdłuż istniejących krawędzi.",
        "Wskazówka: Naciśnij K w Trybie Edycji dla noża (Knife), C aby przecinać na wylot, a Z dla blokady kąta.",
        "Wskazówka: Użyj Ctrl + Shift + B, aby sfazować (Bevel) pojedyncze wierzchołki zamiast krawędzi.",
        "Wskazówka: Zaznaczaj pętle krawędzi (Edge Loops) przytrzymując Alt + Kliknięcie.",
        "Wskazówka: Naciśnij Alt + E w Trybie Edycji, aby otworzyć zaawansowane menu wytłaczania (Extrude).",
        "Wskazówka: Naciśnij Shift + N w Trybie Edycji, aby przeliczyć wektory normalne na zewnątrz (Recalculate Normals).",
        "Wskazówka: W Cycles ustaw Noise Threshold w sekcji Sampling, aby drastycznie przyspieszyć renderowanie.",
        "Wskazówka: Użyj profilu kolorów AgX w sekcji Color Management dla realistycznych przejść tonalnych!",
        "Wskazówka: Włącz odszumianie (OpenImageDenoise lub OptiX) w ustawieniach Cycles dla czystego obrazu.",
        "Wskazówka: Użyj węzła Ray Portal BSDF w Cycles do tworzenia bezszwowych portali i zakrzywień światła!",
        "Wskazówka: Użyj Light Groups w Cycles, aby dostosować jasność poszczególnych świateł po renderze!",
        "Wskazówka: Użyj przebiegu Cryptomatte w Cycles do automatycznego generowania masek obiektów i materiałów.",
        "Wskazówka: Włącz Odbicia w Przestrzeni Ekranu (SSR) i Subsurface Scattering w EEVEE Next dla realizmu.",
        "Wskazówka: Naciśnij Shift + E w Graph Editorze, aby ustawić ekstrapolację krzywych (Linear, Make Cyclic).",
        "Wskazówka: Kliknij prawym na dowolną właściwość i wybierz Add Driver, aby używać wyrażeń Python!",
        "Wskazówka: Dodaj więz Kinematyki Odwrotnej (IK) do kości, aby naturalnie pozować ręce i nogi postaci.",
        "Wskazówka: Naciśnij Stash lub Push Down w Dope Sheet, aby przenieść akcje animacji do edytora NLA.",
        "Wskazówka: Użyj Shape Keys we właściwościach siatki, aby tworzyć klawisze kształtu i mimikę twarzy.",
        "Wskazówka: Naciśnij Ctrl + Tab przy zaznaczonej armaturze, aby błyskawicznie przejść do Pozowania (Pose Mode).",
        "Wskazówka: Włącz Dyntopo (Dynamic Topology) w Sculpt Mode, aby siatka automatycznie zagęszczała się podczas rzeźbienia!",
        "Wskazówka: Naciśnij Ctrl + R w Trybie Rzeźbienia, aby wykonać Voxel Remesh i odświeżyć siatkę.",
        "Wskazówka: Użyj modyfikatora Multiresolution do rzeźbienia drobnych detali z zachowaniem niskopoligonowej bazy.",
        "Wskazówka: Przytrzymaj Shift w Trybie Rzeźbienia z dowolnym pędzlem, aby gładko rozcierać i wygładzać nierówności.",
        "Wskazówka: Użyj Zestawów Ścian (Face Sets pod W) w Sculpt Mode, aby izolować fragmenty siatki podczas rzeźbienia.",
        "Wskazówka: Włącz Głębię Ostrości (Depth of Field) w kamerze i wskaż obiekt ostrości dla filmowego efektu rozmycia.",
        "Wskazówka: Zmień ogniskową obiektywu na 85mm lub 135mm dla portretów bez zniekształceń perspektywicznych.",
        "Wskazówka: Włącz linie pomocnicze (Rule of Thirds, Golden Ratio) w ustawieniach wyświetlania Kamery.",
        "Wskazówka: Naciśnij Ctrl + B w widoku kamery, aby zaznaczyć obszar renderowania i renderować tylko ten fragment!",
        "Wskazówka: Naciśnij Ctrl + Alt + NumPad 0, aby wyrównać aktywną kamerę bezpośrednio do widoku perspektywy.",
        "Wskazówka: Użyj Alt + D do tworzenia Połączonych Duplikatów (Linked Duplicates)—dzielą geometrię i oszczędzają RAM!",
        "Wskazówka: Użyj Instancji Kolekcji (Collection Instances) do powielania rekwizytów tysiące razy bez spadku FPS.",
        "Wskazówka: Naciśnij Ctrl + L, aby szybko kopiować materiały, modyfikatory lub animacje między obiektami.",
        "Wskazówka: Użyj modyfikatora Decimate, aby szybko zredukować liczbę wielokątów w obiektach tła.",
        "Wskazówka: Naciśnij Shift + C, aby wycentrować kursor 3D do środka świata (0,0,0) i dopasować widok."
    ]
}

# --- TUTORIAL DEFINITIONS ---
TUTORIALS = {
    # 1. Podstawowe
    "intro": {
        "title": {"EN": "Intro to Blender", "PL": "Wprowadzenie do Blendera"},
        "steps": [
            {
                "text": {
                    "EN": "Welcome to Blender! I am Clipper. Let's learn the basics. First, select the default Cube in the scene by left-clicking it.",
                    "PL": "Witaj w Blenderze! Jestem Clipper. Nauczmy się podstaw. Najpierw zaznacz domyślną Kostkę w scenie lewym przyciskiem myszy."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.name.startswith("Cube") and ctx.active_object.select_get()
            },
            {
                "text": {
                    "EN": "Great! Let's rename it to 'MyBox'. Press F2, type 'MyBox' and press Enter.",
                    "PL": "Świetnie! Zmieńmy jej nazwę na 'MyBox'. Naciśnij F2, wpisz 'MyBox' i naciśnij Enter."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.name == "MyBox"
            },
            {
                "text": {
                    "EN": "Excellent! Now let's enter Edit Mode to modify its geometry. Press Tab on your keyboard.",
                    "PL": "Doskonale! Wejdźmy w Tryb Edycji, aby zmodyfikować geometrię. Naciśnij Tab na klawiaturze."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'EDIT_MESH'
            },
            {
                "text": {
                    "EN": "Awesome! Let's change selection mode. Press '3' (top row, not Numpad) to switch to Face Selection mode.",
                    "PL": "Super! Zmieńmy tryb zaznaczania. Naciśnij klawisz '3' (górny rząd, nie NumPad), aby przejść do Zaznaczania Ścian."
                },
                "check": lambda ctx: hasattr(ctx, 'tool_settings') and ctx.tool_settings.mesh_select_mode[2] == True
            },
            {
                "text": {
                    "EN": "Superb! Let's go back to Object Mode. Press Tab again.",
                    "PL": "Wspaniale! Wróćmy do Trybu Obiektowego. Naciśnij ponownie klawisz Tab."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Congratulations! You completed the Blender Intro! Click Done to finish.",
                    "PL": "Gratulacje! Ukończyłeś Wprowadzenie do Blendera! Kliknij Gotowe, aby zakończyć."
                },
                "check": None
            }
        ]
    },
    "cushion": {
        "title": {"EN": "Modeling a Cushion", "PL": "Modelowanie Poduszki"},
        "steps": [
            {
                "text": {
                    "EN": "Let's model a cushion! First, delete the active object to clean up. Press X or Delete.",
                    "PL": "Zmodelujmy poduszkę! Najpierw usuń aktywny obiekt. Naciśnij X lub Delete."
                },
                "check": lambda ctx: not hasattr(ctx, 'active_object') or ctx.active_object is None or (hasattr(ctx, 'scene') and ctx.active_object.name not in ctx.scene.objects)
            },
            {
                "text": {
                    "EN": "Now add a Cylinder mesh. Press Shift+A, go to Mesh, and click Cylinder.",
                    "PL": "Teraz dodaj Walec. Naciśnij Shift+A, przejdź do Mesh i kliknij Cylinder."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH' and ctx.active_object.name.startswith("Cylinder")
            },
            {
                "text": {
                    "EN": "Let's flatten it. Press S, then Z, drag your mouse to scale it flat, and left-click to confirm.",
                    "PL": "Spłaszczmy go. Naciśnij S, potem Z, przesuń mysz, aby go spłaszczyć, i kliknij lewym przyciskiem."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.scale[2] < 0.25
            },
            {
                "text": {
                    "EN": "Perfect. Now enter Edit Mode. Press Tab.",
                    "PL": "Idealnie. Teraz wejdź w Tryb Edycji. Naciśnij Tab."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'EDIT_MESH'
            },
            {
                "text": {
                    "EN": "Let me round the edges. Press A to select everything. Then press Ctrl+B, move the mouse out, and scroll your wheel to add segments. Left-click to confirm.",
                    "PL": "Zaokrąglijmy krawędzie. Naciśnij A, aby zaznaczyć wszystko. Następnie Ctrl+B, przesuń mysz i użyj rolki, aby dodać podziały. Kliknij lewym."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object, 'data') and len(ctx.active_object.data.vertices) > 64
            },
            {
                "text": {
                    "EN": "Looking good! Let me return to Object Mode (Tab) and Shade Smooth. Right-click the cylinder and click Shade Smooth.",
                    "PL": "Wygląda świetnie! Wróć do Trybu Obiektowego (Tab), kliknij walec prawym i wybierz Shade Smooth."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'OBJECT' and hasattr(ctx, 'active_object') and ctx.active_object is not None and any(f.use_smooth for f in ctx.active_object.data.polygons)
            },
            {
                "text": {
                    "EN": "Fantastic work! You've modeled a smooth cushion base. Click Done to finish.",
                    "PL": "Fantastyczna robota! Zmodelowałeś bazę gładkiej poduszki. Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "lighting": {
        "title": {"EN": "Lighting & Camera", "PL": "Oświetlenie i Kamera"},
        "steps": [
            {
                "text": {
                    "EN": "Let's set up lighting! Add a Point Light to your scene. Press Shift+A -> Light -> Point Light.",
                    "PL": "Ustawmy oświetlenie! Dodaj światło punktowe. Naciśnij Shift+A -> Light -> Point."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'LIGHT'
            },
            {
                "text": {
                    "EN": "Great! Move the light higher above your scene. Press G, then Z, move your mouse upwards, and click.",
                    "PL": "Świetnie! Przesuń światło wyżej nad scenę. Naciśnij G, potem Z, przesuń mysz w górę i kliknij."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.location[2] > 2.5
            },
            {
                "text": {
                    "EN": "Now select the scene Camera. Click the camera object in the Viewport or Outliner.",
                    "PL": "Teraz zaznacz Kamerę sceny. Kliknij obiekt kamery w widoku lub w oknie Outliner."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'CAMERA'
            },
            {
                "text": {
                    "EN": "Let's snap the camera to your current 3D view. Position your view, then press Ctrl + Alt + NumPad 0!",
                    "PL": "Dopasujmy kamerę do obecnego widoku. Ustaw widok, a następnie naciśnij Ctrl + Alt + NumPad 0!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Awesome! You've mastered lighting and camera positioning! Click Done to finish.",
                    "PL": "Niesamowite! Opanowałeś pozycjonowanie światła i kamery! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "materials": {
        "title": {"EN": "Materials & Shading", "PL": "Materiały i Cieniowanie"},
        "steps": [
            {
                "text": {
                    "EN": "Let me show you how to color objects! First, select any Mesh object in your scene.",
                    "PL": "Pokażę Ci jak pokolorować obiekty! Najpierw zaznacz dowolną Siatkę (Mesh) w scenie."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Now open the Material Properties tab (red sphere icon) and click 'New' to add a material slot.",
                    "PL": "Otwórz zakładkę Właściwości Materiału (czerwona kulka) i kliknij 'New', aby dodać materiał."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object.data, 'materials') and len(ctx.active_object.data.materials) > 0
            },
            {
                "text": {
                    "EN": "Let's view the material! Hold Z and select 'Material Preview' shading mode.",
                    "PL": "Zobaczmy materiał! Przytrzymaj Z i wybierz tryb 'Material Preview'."
                },
                "check": lambda ctx: hasattr(ctx, 'space_data') and ctx.space_data is not None and hasattr(ctx.space_data, 'shading') and ctx.space_data.shading.type in {'MATERIAL', 'RENDERED'}
            },
            {
                "text": {
                    "EN": "Great! Now click 'Base Color' in Material Properties and pick your favorite color!",
                    "PL": "Super! Kliknij 'Base Color' we właściwościach materiału i wybierz swój ulubiony kolor!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Beautiful! You now know how to apply materials and preview shaders! Click Done to finish.",
                    "PL": "Pięknie! Wiesz już jak nakładać materiały i podglądać shadery! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "extrude": {
        "title": {"EN": "Inset & Extrude", "PL": "Wcinanie i Wytłaczanie"},
        "steps": [
            {
                "text": {
                    "EN": "Let me teach you Inset and Extrude! Select a Mesh object and press Tab to enter Edit Mode.",
                    "PL": "Nauczę Cię operacji Inset i Extrude! Zaznacz Siatkę i naciśnij Tab, aby wejść w Tryb Edycji."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'EDIT_MESH'
            },
            {
                "text": {
                    "EN": "Switch to Face Selection mode by pressing key '3' (top number row).",
                    "PL": "Przełącz na Zaznaczanie Ścian wciskając klawisz '3' (górny rząd cyfr)."
                },
                "check": lambda ctx: hasattr(ctx, 'tool_settings') and ctx.tool_settings.mesh_select_mode[2] == True
            },
            {
                "text": {
                    "EN": "Select any face on your object, then press 'I' to Inset the face inward, then left-click.",
                    "PL": "Zaznacz dowolną ścianę obiektu, naciśnij 'I', aby wciąć ścianę do środka, i kliknij lewym."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "With that face selected, press 'E' to Extrude it outwards or inwards, then left-click to place.",
                    "PL": "Mając zaznaczoną ścianę, naciśnij 'E', aby ją wyciągnąć (wytłoczyć) i kliknij lewym."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Tab to return to Object Mode.",
                    "PL": "Naciśnij Tab, aby wrócić do Trybu Obiektowego."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Masterclass complete! Inset (I) and Extrude (E) are essential modeling tools! Click Done to finish.",
                    "PL": "Lekcja zakończona! Inset (I) oraz Extrude (E) to podstawowe narzędzia modelowania! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "sculpting": {
        "title": {"EN": "Sculpting Basics", "PL": "Podstawy Rzeźbienia"},
        "steps": [
            {
                "text": {
                    "EN": "Let's sculpt! Select a Mesh object and switch to Sculpt Mode (top left mode menu).",
                    "PL": "Rzeźbijmy! Zaznacz Siatkę i przejdź do Trybu Rzeźbienia (Sculpt Mode w lewym górnym menu)."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'SCULPT'
            },
            {
                "text": {
                    "EN": "Press 'F' to adjust the sculpting brush size, move mouse and click to confirm.",
                    "PL": "Naciśnij 'F', aby zmienić rozmiar pędzla rzeźbiarskiego, przesuń mysz i kliknij."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Shift+'F' to adjust brush strength, move mouse and click.",
                    "PL": "Naciśnij Shift+'F', aby dostosować siłę pędzla, przesuń mysz i kliknij."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Click and drag across the mesh surface to sculpt 3D detail!",
                    "PL": "Kliknij i przeciągnij po powierzchni siatki, aby rzeźbić detale 3D!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Switch mode back to Object Mode.",
                    "PL": "Przełącz tryb z powrotem na Tryb Obiektowy."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Awesome! Sculpting lets you craft organic 3D shapes freely! Click Done to finish.",
                    "PL": "Niesamowite! Rzeźbienie pozwala swobodnie tworzyć organiczne kształty! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "modifiers": {
        "title": {"EN": "Subdivision Surface", "PL": "Modyfikator Subdivision"},
        "steps": [
            {
                "text": {
                    "EN": "Let's learn Modifiers! Select any Mesh object in Object Mode.",
                    "PL": "Poznajmy Modyfikatory! Zaznacz dowolną Siatkę w Trybie Obiektowym."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Modifier Properties (blue wrench icon) and click Add Modifier.",
                    "PL": "Otwórz Właściwości Modyfikatorów (niebieski klucz) i kliknij Dodaj Modyfikator."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Add a Subdivision Surface modifier (or shortcut Ctrl+2).",
                    "PL": "Dodaj modyfikator Subdivision Surface (lub użyj skrótu Ctrl+2)."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object, 'modifiers') and any(m.type == 'SUBSURF' for m in ctx.active_object.modifiers)
            },
            {
                "text": {
                    "EN": "Notice how smooth your mesh becomes! Increase Viewport Levels to 2.",
                    "PL": "Zobacz jak gładki staje się obiekt! Zwiększ poziom podziału (Viewport Levels) do 2."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Subdivision Surface non-destructively smoothes 3D geometry! Click Done to finish.",
                    "PL": "Subdivision Surface elastycznie wygładza geometrię 3D! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "animation": {
        "title": {"EN": "Keyframe Animation", "PL": "Animacja Kluczowa"},
        "steps": [
            {
                "text": {
                    "EN": "Let me teach you Keyframe Animation! Select an object and ensure Timeline playhead is at frame 1.",
                    "PL": "Nauczę Cię Animacji Kluczowej! Zaznacz obiekt i upewnij się, że czas jest na klatce 1."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx, 'scene') and ctx.scene.frame_current == 1
            },
            {
                "text": {
                    "EN": "Press 'I' in 3D Viewport to open Insert Keyframe menu, and click Location.",
                    "PL": "Naciśnij 'I' w widoku 3D, aby otworzyć menu klatek kluczowych i wybierz Location (Położenie)."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.animation_data is not None
            },
            {
                "text": {
                    "EN": "Drag your Timeline slider at bottom to frame 40.",
                    "PL": "Przesuń suwak osi czasu na dole do klatki 40."
                },
                "check": lambda ctx: hasattr(ctx, 'scene') and ctx.scene.frame_current >= 30
            },
            {
                "text": {
                    "EN": "Move your object to a new location (G), then press 'I' and select Location again!",
                    "PL": "Przesuń obiekt w nowe miejsce (G), a następnie naciśnij 'I' i wybierz ponownie Location!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Spacebar to play your keyframe animation!",
                    "PL": "Naciśnij Spację, aby odtworzyć utworzoną animację!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Fantastic! You've animated your first 3D object in Blender! Click Done to finish.",
                    "PL": "Fantastycznie! Zaanimowałeś swój pierwszy obiekt 3D w Blenderze! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "uv_unwrap": {
        "title": {"EN": "UV Unwrapping", "PL": "Rozwijanie UV"},
        "steps": [
            {
                "text": {
                    "EN": "Let's learn UV Unwrapping! Select a Mesh object and enter Edit Mode (Tab).",
                    "PL": "Nauczmy się Rozwijania UV! Zaznacz Siatkę i wejdź w Tryb Edycji (Tab)."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'EDIT_MESH'
            },
            {
                "text": {
                    "EN": "Press 'A' to select all vertices and faces.",
                    "PL": "Naciśnij 'A', aby zaznaczyć wszystkie wierzchołki i ściany."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press 'U' to open the UV Mapping menu.",
                    "PL": "Naciśnij 'U', aby otworzyć menu Mapowania UV."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Click 'Smart UV Project' and press OK to auto-unwrap your mesh.",
                    "PL": "Kliknij 'Smart UV Project' i naciśnij OK, aby automatycznie rozwinąć siatkę."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Tab to return to Object Mode.",
                    "PL": "Naciśnij Tab, aby wrócić do Trybu Obiektowego."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Great job! UV unwrapping projects 2D textures onto 3D surfaces! Click Done to finish.",
                    "PL": "Świetna robota! Rozwijanie UV pozwala nakładać tekstury 2D na obiekty 3D! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "nodes": {
        "title": {"EN": "Shader Nodes", "PL": "Węzły Shadera"},
        "steps": [
            {
                "text": {
                    "EN": "Let me show you Shader Nodes! Switch to the Shading workspace tab at top.",
                    "PL": "Pokażę Ci Węzły Shadera! Przełącz się na zakładkę Shading na samej górze."
                },
                "check": lambda ctx: (hasattr(ctx, 'workspace') and ctx.workspace is not None and ctx.workspace.name == 'Shading') or (hasattr(ctx, 'space_data') and ctx.space_data is not None and hasattr(ctx.space_data, 'tree_type') and ctx.space_data.tree_type == 'ShaderNodeTree')
            },
            {
                "text": {
                    "EN": "Select your object and click 'New' in the Shader Editor panel.",
                    "PL": "Zaznacz obiekt i kliknij 'New' w panelu Edytora Shaderów."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.active_material is not None
            },
            {
                "text": {
                    "EN": "Inside Shader Editor, press Shift+A -> Texture -> Noise Texture to add a noise node.",
                    "PL": "W Edytorze Shaderów naciśnij Shift+A -> Texture -> Noise Texture, aby dodać węzeł szumu."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Connect Color output of Noise Texture to Base Color of Principled BSDF.",
                    "PL": "Połącz wyjście Color z Noise Texture z wejściem Base Color węzła Principled BSDF."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Hold Z and switch to Material Preview to see your procedural texture pattern!",
                    "PL": "Przytrzymaj Z i przełącz na Podgląd Materiału, aby zobaczyć proceduralny wzór!"
                },
                "check": lambda ctx: hasattr(ctx, 'space_data') and ctx.space_data is not None and hasattr(ctx.space_data, 'shading') and ctx.space_data.shading.type in {'MATERIAL', 'RENDERED'}
            },
            {
                "text": {
                    "EN": "Masterclass complete! Shader nodes unlock unlimited materials! Click Done to finish.",
                    "PL": "Lekcja zakończona! Węzły shadera dają nieograniczone możliwości! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "cloth": {
        "title": {"EN": "Cloth Simulation", "PL": "Symulacja Tkaniny"},
        "steps": [
            {
                "text": {
                    "EN": "Let's create a cloth simulation! First, add a Grid mesh to your scene. Press Shift+A -> Mesh -> Grid.",
                    "PL": "Stwórzmy symulację tkaniny! Najpierw dodaj siatkę Grid. Naciśnij Shift+A -> Mesh -> Grid."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH' and ctx.active_object.name.startswith("Grid")
            },
            {
                "text": {
                    "EN": "Move the grid higher above your scene floor. Press G, then Z, move upwards and click.",
                    "PL": "Przesuń siatkę wyżej nad podłogę sceny. Naciśnij G, potem Z, przesuń w górę i kliknij."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.location[2] > 2.0
            },
            {
                "text": {
                    "EN": "Open Physics Properties (blue orbital atom icon on right panel) and click 'Cloth'.",
                    "PL": "Otwórz Właściwości Fizyki (niebieski atom po prawej) i kliknij 'Cloth' (Tkanina)."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object, 'modifiers') and any(m.type == 'CLOTH' for m in ctx.active_object.modifiers)
            },
            {
                "text": {
                    "EN": "Press Spacebar to play the physics animation and watch your cloth drop and drape!",
                    "PL": "Naciśnij Spację, aby odtworzyć animację fizyki i zobaczyć jak tkanina opada!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Awesome! You've created a dynamic 3D cloth simulation! Click Done to finish.",
                    "PL": "Niesamowite! Stworzyłeś dynamiczną symulację tkaniny 3D! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "particles": {
        "title": {"EN": "Particle System", "PL": "System Cząsteczek"},
        "steps": [
            {
                "text": {
                    "EN": "Let's create a particle emitter! Select any Mesh object in your scene.",
                    "PL": "Stwórzmy emiter cząsteczek! Zaznacz dowolną Siatkę (Mesh) w scenie."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Particle Properties (three connected dots icon) and click '+' to add a Particle System.",
                    "PL": "Otwórz Właściwości Cząsteczek (trzy połączone kropki) i kliknij '+', aby dodać system."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object, 'particle_systems') and len(ctx.active_object.particle_systems) > 0
            },
            {
                "text": {
                    "EN": "Press Spacebar to play animation and see particles bursting out from your object!",
                    "PL": "Naciśnij Spację, aby odtworzyć animację i zobaczyć tryskające cząsteczki!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Spectacular! Particle systems are used for sparks, rain, smoke, and hair! Click Done to finish.",
                    "PL": "Widowiskowe! Systemy cząsteczek tworzą deszcz, iskry, dym i włosy! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "grease_pencil": {
        "title": {"EN": "2D Grease Pencil", "PL": "2D Grease Pencil"},
        "steps": [
            {
                "text": {
                    "EN": "Let's draw 2D art in 3D! Add a Blank Grease Pencil object. Press Shift+A -> Grease Pencil -> Blank.",
                    "PL": "Rysujmy 2D w 3D! Dodaj pusty obiekt Grease Pencil. Naciśnij Shift+A -> Grease Pencil -> Blank."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and (ctx.active_object.type == 'GPENCIL' or ctx.active_object.type == 'GREASEPENCIL')
            },
            {
                "text": {
                    "EN": "Switch to Draw Mode using the top-left mode dropdown menu.",
                    "PL": "Przełącz się na Tryb Rysowania (Draw Mode) w lewym górnym menu."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and 'DRAW' in ctx.mode
            },
            {
                "text": {
                    "EN": "Click and drag across the 3D Viewport to draw 2D strokes in 3D space!",
                    "PL": "Kliknij i przeciągnij po widoku 3D, aby rysować pociągnięcia 2D w przestrzeni 3D!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Switch mode back to Object Mode.",
                    "PL": "Przełącz tryb z powrotem na Tryb Obiektowy."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Wonderful! Grease Pencil blends 2D animation directly inside 3D space! Click Done to finish.",
                    "PL": "Wspaniale! Grease Pencil łączy animację 2D z przestrzenią 3D! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "rigid_body": {
        "title": {"EN": "Rigid Body Physics", "PL": "Ciała Sztywne (Rigid Body)"},
        "steps": [
            {
                "text": {
                    "EN": "Let's make objects tumble with gravity! Select any Cube or Mesh in your scene.",
                    "PL": "Sprawmy, by obiekty spadały z grawitacją! Zaznacz dowolną Kostkę lub Siatkę."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Physics Properties (blue atom icon) and click 'Rigid Body'.",
                    "PL": "Otwórz Właściwości Fizyki (niebieski atom) i kliknij 'Rigid Body' (Ciało Sztywne)."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.rigid_body is not None
            },
            {
                "text": {
                    "EN": "Press Spacebar to play animation and watch your object fall with physical gravity!",
                    "PL": "Naciśnij Spację, aby odtworzyć animację i zobaczyć jak obiekt spada z grawitacją!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Great job! Rigid Body physics powers realistic collisions and destructions! Click Done to finish.",
                    "PL": "Świetna robota! Fizyka Rigid Body tworzy realistyczne zderzenia i zniszczenia! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "bevel_modifier": {
        "title": {"EN": "Bevel Modifier", "PL": "Modyfikator Bevel"},
        "steps": [
            {
                "text": {
                    "EN": "Let's round mesh edges non-destructively! Select a Cube mesh in Object Mode.",
                    "PL": "Zaokrąglijmy krawędzie siatki elastycznie! Zaznacz Kostkę w Trybie Obiektowym."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Modifier Properties (blue wrench icon) and click Add Modifier -> Bevel.",
                    "PL": "Otwórz Właściwości Modyfikatorów (niebieski klucz) i dodaj modyfikator Bevel (Faza)."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object, 'modifiers') and any(m.type == 'BEVEL' for m in ctx.active_object.modifiers)
            },
            {
                "text": {
                    "EN": "Increase the Segments slider to 3 or 4 to catch smooth realistic highlights on edges!",
                    "PL": "Zwiększ suwak Segments do 3 lub 4, aby uzyskać gładkie, realistyczne odblaski na krawędziach!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Excellent! Hard edges don't exist in nature—always use Bevel for realism! Click Done to finish.",
                    "PL": "Doskonale! Ostre krawędzie nie istnieją w naturze—zawsze używaj Bevel dla realizmu! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    # 2. Zaawansowane Poradniki (Advanced Tutorials)
    "geom_nodes": {
        "title": {"EN": "⚡ Geometry Nodes Procedural", "PL": "⚡ Geometry Nodes (Proceduralne)"},
        "steps": [
            {
                "text": {
                    "EN": "Let's explore procedural generation! Select any Mesh object in Object Mode.",
                    "PL": "Odkryjmy generowanie proceduralne! Zaznacz dowolną Siatkę (Mesh) w Trybie Obiektowym."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Modifier Properties (blue wrench) and click Add Modifier -> Geometry Nodes.",
                    "PL": "Otwórz Właściwości Modyfikatorów (niebieski klucz) i dodaj modyfikator Geometry Nodes."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object, 'modifiers') and any(m.type == 'NODES' for m in ctx.active_object.modifiers)
            },
            {
                "text": {
                    "EN": "Switch to the Geometry Nodes workspace tab at the top of Blender UI.",
                    "PL": "Przełącz się na zakładkę obszaru roboczego Geometry Nodes na samej górze."
                },
                "check": lambda ctx: (hasattr(ctx, 'workspace') and ctx.workspace is not None and ctx.workspace.name == 'Geometry Nodes') or (hasattr(ctx, 'space_data') and ctx.space_data is not None and hasattr(ctx.space_data, 'tree_type') and ctx.space_data.tree_type == 'GeometryNodeTree')
            },
            {
                "text": {
                    "EN": "Inside Geometry Node Editor, press Shift+A -> Geometry -> Set Position to add a transformation node!",
                    "PL": "W Edytorze Geometry Nodes naciśnij Shift+A -> Geometry -> Set Position, aby dodać węzeł modyfikacji pozycji!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Outstanding! Geometry Nodes powers procedural city generation, foliage scattering, and dynamic FX! Click Done to finish.",
                    "PL": "Wybitnie! Geometry Nodes pozwala tworzyć proceduralne miasta, rozsiewać roślinność oraz efekty FX! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "hard_surface": {
        "title": {"EN": "⚡ Advanced Hard Surface", "PL": "⚡ Zaawansowany Hard Surface"},
        "steps": [
            {
                "text": {
                    "EN": "Let's master CAD-style Hard Surface modeling! Select any Mesh object in Object Mode.",
                    "PL": "Opanujmy modelowanie Hard Surface w stylu CAD! Zaznacz dowolną Siatkę w Trybie Obiektowym."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Add a Boolean modifier to perform non-destructive mesh cuts. (Modifier Properties -> Add -> Boolean).",
                    "PL": "Dodaj modyfikator Boolean do elastycznego wycinania kształtów (Modyfikatory -> Dodaj -> Boolean)."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object, 'modifiers') and any(m.type == 'BOOLEAN' for m in ctx.active_object.modifiers)
            },
            {
                "text": {
                    "EN": "Add a Weighted Normal modifier to sharpen flat surfaces and fix shading artifacts seamlessly!",
                    "PL": "Dodaj modyfikator Weighted Normal, aby naprawić cieniowanie i uzyskać czyste odblaski!"
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object, 'modifiers') and any(m.type == 'WEIGHTED_NORMAL' for m in ctx.active_object.modifiers)
            },
            {
                "text": {
                    "EN": "Enter Edit Mode (Tab), press 'K' for Knife tool, and press 'C' to cut through geometry completely!",
                    "PL": "Wejdź w Tryb Edycji (Tab), naciśnij 'K' dla noża oraz 'C', aby przecinać geometrię na wylot!"
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'EDIT_MESH'
            },
            {
                "text": {
                    "EN": "Press Tab to return to Object Mode.",
                    "PL": "Naciśnij Tab, aby wrócić do Trybu Obiektowego."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Incredible! Combining Booleans, Weighted Normals, and Bevel forms the core of pro sci-fi asset creation! Click Done to finish.",
                    "PL": "Niesamowite! Łączenie Boolean, Weighted Normals i Bevel to podstawa profesjonalnego tworzenia aktywów sci-fi! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "drivers": {
        "title": {"EN": "⚡ Drivers & Automation", "PL": "⚡ Sterowniki i Automatyzacja (Drivers)"},
        "steps": [
            {
                "text": {
                    "EN": "Let's automate properties with Drivers! Select any object in your 3D Viewport.",
                    "PL": "Zautomatyzujmy właściwości za pomocą Sterowników! Zaznacz dowolny obiekt w widoku 3D."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None
            },
            {
                "text": {
                    "EN": "Open Object Properties (orange square icon) on the right sidebar.",
                    "PL": "Otwórz Właściwości Obiektu (pomarańczowy kwadrat) w prawym panelu."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Right-click on Rotation Z and click 'Add Driver'.",
                    "PL": "Kliknij prawym przyciskiem myszy na Rotation Z (Obrót Z) i wybierz 'Add Driver'."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Type a Python expression like `frame / 10` to drive rotation smoothly over time!",
                    "PL": "Wpisz wyrażenie Python takie jak `frame / 10`, aby obiekt obracał się wraz z meczą czasu!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Spacebar to play animation and see your driven object rotate automatically!",
                    "PL": "Naciśnij Spację, aby odtworzyć animację i zobaczyć automatyczny obrót!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Genius! Drivers link complex mechanical gears, custom UI controls, and rig logic using math! Click Done to finish.",
                    "PL": "Genialne! Sterowniki łączą koła zębate, suwaki interfejsu oraz logikę rigów za pomocą matematyki! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "rigging_ik": {
        "title": {"EN": "⚡ Character Rigging & IK", "PL": "⚡ Rigging i Kinematyka Odwrotna (IK)"},
        "steps": [
            {
                "text": {
                    "EN": "Let's rig a character skeleton! Add a single bone Armature. Press Shift+A -> Armature.",
                    "PL": "Zbudujmy szkielet postaci! Dodaj nową kość. Naciśnij Shift+A -> Armature."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'ARMATURE'
            },
            {
                "text": {
                    "EN": "Enter Edit Mode (Tab), select the top tip of the bone, and press 'E' to extrude a second bone segment upward.",
                    "PL": "Wejdź w Tryb Edycji (Tab), zaznacz górną końcówkę kości i naciśnij 'E', aby wyciągnąć kolejną kość w górę."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'EDIT_ARMATURE'
            },
            {
                "text": {
                    "EN": "Switch to Pose Mode by pressing Ctrl+Tab (or dropdown menu).",
                    "PL": "Przełącz się na Tryb Pozowania (Pose Mode) wciskając Ctrl+Tab."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'POSE'
            },
            {
                "text": {
                    "EN": "Open Bone Constraint Properties (bone with chain icon) and click Add Bone Constraint -> Inverse Kinematics (IK).",
                    "PL": "Otwórz Właściwości Więzów Kości (kość z łańcuchem) i dodaj Inverse Kinematics (IK)."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Move the IK target bone (G) and watch the entire bone chain bend organically like a real limb!",
                    "PL": "Przesuń kość docelową IK (G) i zobacz jak cały łańcuch kości zgina się jak prawdziwa kończyna!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Mastery unlocked! Inverse Kinematics is the foundation of 3D character animation! Click Done to finish.",
                    "PL": "Poziom opanowany! Kinematyka Odwrotna to podstawa animacji postaci 3D! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "cycles_opt": {
        "title": {"EN": "⚡ Cycles Render & AgX", "PL": "⚡ Renderowanie Cycles i Barwa AgX"},
        "steps": [
            {
                "text": {
                    "EN": "Let's configure photorealistic rendering! Open Render Properties (camera icon) and set Render Engine to Cycles.",
                    "PL": "Skonfigurujmy fotorealistyczny render! Otwórz Właściwości Renderowania (ikona aparatu) i zmień silnik na Cycles."
                },
                "check": lambda ctx: hasattr(ctx, 'scene') and ctx.scene is not None and hasattr(ctx.scene, 'render') and ctx.scene.render.engine == 'CYCLES'
            },
            {
                "text": {
                    "EN": "Under Sampling -> Viewport, check Noise Threshold and set Max Samples to 256 for blazing fast noisy noise reduction.",
                    "PL": "W sekcji Sampling -> Viewport zaznacz Noise Threshold i ustaw Max Samples na 256 dla szybkiego podglądu."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Scroll down to Color Management panel and set View Transform to AgX.",
                    "PL": "Przewiń na dół do panelu Color Management i zmień View Transform na AgX."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Hold Z and select 'Rendered' to view photorealistic lighting with natural highlight roll-offs!",
                    "PL": "Przytrzymaj Z i wybierz 'Rendered', aby zobaczyć fotorealistyczne światło z płynnymi przejściami tonalnymi!"
                },
                "check": lambda ctx: hasattr(ctx, 'space_data') and ctx.space_data is not None and hasattr(ctx.space_data, 'shading') and ctx.space_data.shading.type == 'RENDERED'
            },
            {
                "text": {
                    "EN": "Phenomenal! AgX color management gives film-grade color science without clipped highlights! Click Done to finish.",
                    "PL": "Fenomenalnie! Kolorometria AgX zapewnia filmowy wygląd bez przepalonych bieli! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "sculpt_remesh": {
        "title": {"EN": "⚡ Voxel Remesh & Dyntopo", "PL": "⚡ Voxel Remesh i Dyntopo"},
        "steps": [
            {
                "text": {
                    "EN": "Let's master high-resolution sculpt workflows! Select any Mesh and enter Sculpt Mode.",
                    "PL": "Opanujmy zaawansowane rzeźbienie! Zaznacz dowolną Siatkę i wejdź w Tryb Rzeźbienia (Sculpt Mode)."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'SCULPT'
            },
            {
                "text": {
                    "EN": "Look at the top bar for 'Remesh'. Set Voxel Size to 0.05 m and click the Remesh button (or press Ctrl+R).",
                    "PL": "Spójrz na górny pasek na opcję 'Remesh'. Ustaw Voxel Size na 0.05 m i kliknij Remesh (lub naciśnij Ctrl+R)."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Select the Snake Hook or Clay Strips brush from the left toolbar and pull out dramatic forms!",
                    "PL": "Wybierz pędzel Snake Hook lub Clay Strips z lewego paska i wyciągnij odważne kształty!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press Ctrl+R again anytime geometry stretches to rebuild clean uniform voxels!",
                    "PL": "Naciśnij Ctrl+R ponownie w dowolnym momencie, aby odświeżyć i zagęścić siatkę!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Brilliant! Voxel Remesh lets concept artists sculpt complex creatures without topological limitations! Click Done to finish.",
                    "PL": "Gienialnie! Voxel Remesh pozwala rzeźbić dowolne stwory bez ograniczeń topologii! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "shape_keys": {
        "title": {"EN": "⚡ Shape Keys & Morphing", "PL": "⚡ Shape Keys i Morphing Twarzy"},
        "steps": [
            {
                "text": {
                    "EN": "Let's create 3D morphing targets! Select a Mesh object and open Object Data Properties (green mesh icon).",
                    "PL": "Stwórzmy cele morfingu 3D! Zaznacz Siatkę i otwórz Właściwości Danych Obiektu (zielona siatka)."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "In Shape Keys panel, click '+' once to create 'Basis', then click '+' again to add 'Key 1'.",
                    "PL": "W panelu Shape Keys kliknij '+' raz, aby utworzyć 'Basis', a następnie '+' ponownie dla 'Key 1'."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and hasattr(ctx.active_object.data, 'shape_keys') and ctx.active_object.data.shape_keys is not None and len(ctx.active_object.data.shape_keys.key_blocks) >= 2
            },
            {
                "text": {
                    "EN": "With 'Key 1' selected, press Tab to enter Edit Mode, grab vertices to reshape the mesh, then return to Object Mode (Tab).",
                    "PL": "Mając zaznaczony 'Key 1', naciśnij Tab (Tryb Edycji), zniekształć wierzchołki i wróć do Trybu Obiektowego (Tab)."
                },
                "check": lambda ctx: hasattr(ctx, 'mode') and ctx.mode == 'OBJECT'
            },
            {
                "text": {
                    "EN": "Drag the 'Value' slider of Key 1 from 0.0 to 1.0 to watch your mesh smoothly morph!",
                    "PL": "Przeciągnij suwak 'Value' klawisza Key 1 od 0.0 do 1.0, aby zobaczyć płynny morfing!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Outstanding! Shape Keys drive facial expressions, lip-syncing, winks, and muscle bulging! Click Done to finish.",
                    "PL": "Znakomicie! Shape Keys odpowiadają za ekspresję twarzy, ruchy ust, mruganie i praca mięśni! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "graph_editor": {
        "title": {"EN": "⚡ Graph Editor Curves", "PL": "⚡ Krzywe Animacji (Graph Editor)"},
        "steps": [
            {
                "text": {
                    "EN": "Let's master organic motion easing! Ensure an animated object exists in your scene.",
                    "PL": "Opanujmy płynność i dynamikę ruchu! Upewnij się, że masz zaanimowany obiekt w scenie."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.animation_data is not None
            },
            {
                "text": {
                    "EN": "Switch to the Animation workspace tab at top or open the Graph Editor window.",
                    "PL": "Przełącz się na zakładkę obszaru roboczego Animation na górze lub otwórz okno Graph Editor."
                },
                "check": lambda ctx: (hasattr(ctx, 'workspace') and ctx.workspace is not None and ctx.workspace.name == 'Animation') or (hasattr(ctx, 'space_data') and ctx.space_data is not None and hasattr(ctx.space_data, 'type') and ctx.space_data.type == 'GRAPH_EDITOR')
            },
            {
                "text": {
                    "EN": "Select keyframe handles in the Graph Editor, press 'V' and set Handle Type to Free or Vector.",
                    "PL": "Zaznacz uchwyty kluczy w Graph Editorze, naciśnij 'V' i wybierz typ uchwytu (Free lub Vector)."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Press 'T' to change interpolation mode between Constant, Linear, Bezier, and Bounce easing curves!",
                    "PL": "Naciśnij 'T', aby zmienić tryb interpolacji między Bezier, Linear, Constant i Bounce!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "World-class skill unlocked! Graph Editor bezier handles give complete artistic authority over motion velocity! Click Done to finish.",
                    "PL": "Mistrzowski poziom! Krzywe Beziera dają pełną kontrolę nad prędkością i akceleracją animacji! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "baking_maps": {
        "title": {"EN": "⚡ Texture Baking (Normal & AO)", "PL": "⚡ Wypalanie Tekstur (Normal & AO)"},
        "steps": [
            {
                "text": {
                    "EN": "Let's bake high-poly details into low-poly game maps! Set render engine to Cycles (Render Properties -> Engine -> Cycles).",
                    "PL": "Wypalmy detale high-poly na siatkę low-poly! Ustaw silnik na Cycles (Właściwości Renderowania -> Cycles)."
                },
                "check": lambda ctx: hasattr(ctx, 'scene') and ctx.scene is not None and hasattr(ctx.scene, 'render') and ctx.scene.render.engine == 'CYCLES'
            },
            {
                "text": {
                    "EN": "Select your UV-unwrapped target Mesh object.",
                    "PL": "Zaznacz rozłożony w UV obiekt docelowy."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.type == 'MESH'
            },
            {
                "text": {
                    "EN": "Open Shader Editor, press Shift+A -> Texture -> Image Texture, and click 'New' to create a target image.",
                    "PL": "Otwórz Shader Editor, naciśnij Shift+A -> Texture -> Image Texture i kliknij 'New', aby utworzyć nową teksturę."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Keep the Image Texture node selected in Shader Editor (do NOT connect its wires).",
                    "PL": "Upewnij się, że węzeł Image Texture jest zaznaczony (nie musisz go podłączać)."
                },
                "check": None
            },
            {
                "text": {
                    "EN": "In Render Properties, open Bake panel, choose Bake Type 'Normal' or 'Ambient Occlusion', and click Bake!",
                    "PL": "W panelu Render Properties otwórz sekcję Bake, wybierz Normal lub Ambient Occlusion i kliknij Bake!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Awesome! Texture baking translates micro-sculpt surface details into lightweight game engine maps! Click Done to finish.",
                    "PL": "Niesamowite! Wypalanie tekstur zamienia miliony wielokątów w lekkie mapy dla silników gier! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    },
    "nla_animation": {
        "title": {"EN": "⚡ Non-Linear Animation (NLA)", "PL": "⚡ Nieliniowa Animacja (NLA)"},
        "steps": [
            {
                "text": {
                    "EN": "Let's blend multiple animation clips non-destructively! Select an object with existing animation keyframes.",
                    "PL": "Połączmy wiele klipów animacji! Zaznacz obiekt z istniejącymi kluczami animacji."
                },
                "check": lambda ctx: hasattr(ctx, 'active_object') and ctx.active_object is not None and ctx.active_object.animation_data is not None
            },
            {
                "text": {
                    "EN": "Open the Non-Linear Animation (NLA Editor) window from the editor type menu.",
                    "PL": "Otwórz okno Non-Linear Animation (Edytor NLA) z menu typów edytorów."
                },
                "check": lambda ctx: hasattr(ctx, 'space_data') and ctx.space_data is not None and hasattr(ctx.space_data, 'type') and ctx.space_data.type == 'NLA_EDITOR'
            },
            {
                "text": {
                    "EN": "Click the 'Push Down' or 'Stash' icon next to your action to convert keyframes into a moveable NLA strip!",
                    "PL": "Kliknij ikony 'Push Down' lub 'Stash' obok nazwy akcji, aby przekształcić klucze w przesuwny pasek NLA!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Drag, blend, and loop NLA strips across multiple tracks to mix walk cycles, attacks, and facial animation effortlessly!",
                    "PL": "Przesuwaj, mieszaj i pętluj paski NLA na wielu ścieżkach, aby bez wysiłku łączyć biegi, ataki i gesty!"
                },
                "check": None
            },
            {
                "text": {
                    "EN": "Mastery unlocked! The NLA Editor is standard industry workflow for AAA game and film animation blending! Click Done to finish.",
                    "PL": "Mistrzowski poziom! Edytor NLA to standard branżowy w grach AAA oraz filmach! Kliknij Gotowe."
                },
                "check": None
            }
        ]
    }
}

# --- SAFETY REDRAW & CHECK HELPERS ---
def safe_tag_redraw(context):
    try:
        if hasattr(context, "screen") and context.screen and hasattr(context.screen, "areas"):
            for area in context.screen.areas:
                if hasattr(area, "type") and area.type == 'VIEW_3D':
                    area.tag_redraw()
        elif hasattr(context, "area") and context.area and hasattr(context.area, "tag_redraw"):
            context.area.tag_redraw()
    except Exception:
        pass

def safe_check_step(check_func, ctx):
    try:
        return bool(check_func(ctx))
    except Exception:
        return False

# --- PROCEDURAL DRAWING HELPERS ---
def draw_polyline(points, color, width, viewport_size):
    if len(points) < 2:
        return
    gpu.state.blend_set('ALPHA')
    shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": points})
    shader.bind()
    shader.uniform_float("color", color)
    shader.uniform_float("viewportSize", viewport_size)
    shader.uniform_float("lineWidth", width)
    batch.draw(shader)

def get_uniform_color_shader():
    try:
        return gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    except Exception:
        return gpu.shader.from_builtin('UNIFORM_COLOR')

def draw_rect(x, y, w, h, color):
    gpu.state.blend_set('ALPHA')
    shader = get_uniform_color_shader()
    coords = [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    batch = batch_for_shader(shader, 'TRI_STRIP', {"pos": coords})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

def draw_rect_outline(x, y, w, h, color, width, viewport_size):
    coords = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
    draw_polyline(coords, color, width, viewport_size)

def draw_circle(cx, cy, r, color, segments=24):
    gpu.state.blend_set('ALPHA')
    shader = get_uniform_color_shader()
    coords = [(cx, cy)]
    for i in range(segments + 1):
        angle = (i / segments) * (2.0 * math.pi)
        coords.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

def draw_circle_outline(cx, cy, r, color, width, viewport_size, segments=24):
    coords = []
    for i in range(segments + 1):
        angle = (i / segments) * (2.0 * math.pi)
        coords.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    draw_polyline(coords, color, width, viewport_size)

def draw_rounded_rect(x, y, w, h, r, color, segments=8):
    gpu.state.blend_set('ALPHA')
    shader = get_uniform_color_shader()
    r = min(r, w / 2.0, h / 2.0)
    cx, cy = x + w / 2.0, y + h / 2.0
    coords = [(cx, cy)]
    
    def add_arc(acx, acy, start_angle, end_angle):
        for i in range(segments + 1):
            angle = start_angle + (end_angle - start_angle) * (i / segments)
            coords.append((acx + math.cos(angle) * r, acy + math.sin(angle) * r))
            
    add_arc(x + w - r, y + r, 1.5 * math.pi, 2.0 * math.pi)
    add_arc(x + w - r, y + h - r, 0.0, 0.5 * math.pi)
    add_arc(x + r, y + h - r, 0.5 * math.pi, math.pi)
    add_arc(x + r, y + r, math.pi, 1.5 * math.pi)
    coords.append(coords[1])
    
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

def draw_rounded_rect_outline(x, y, w, h, r, color, width, viewport_size, segments=8):
    r = min(r, w / 2.0, h / 2.0)
    coords = []
    
    def add_arc(acx, acy, start_angle, end_angle):
        for i in range(segments + 1):
            angle = start_angle + (end_angle - start_angle) * (i / segments)
            coords.append((acx + math.cos(angle) * r, acy + math.sin(angle) * r))
            
    add_arc(x + w - r, y + r, 1.5 * math.pi, 2.0 * math.pi)
    add_arc(x + w - r, y + h - r, 0.0, 0.5 * math.pi)
    add_arc(x + r, y + h - r, 0.5 * math.pi, math.pi)
    add_arc(x + r, y + r, math.pi, 1.5 * math.pi)
    coords.append(coords[0])
    
    draw_polyline(coords, color, width, viewport_size)

def draw_bubble_pointer(bx, by, px, py, is_left, bw, color, border_color, border_width, viewport_size):
    gpu.state.blend_set('ALPHA')
    if is_left:
        p1 = (px, py)
        p2 = (bx + bw, by + 12)
        p3 = (bx + bw, by + 26)
    else:
        p1 = (px, py)
        p2 = (bx, by + 12)
        p3 = (bx, by + 26)
        
    shader = get_uniform_color_shader()
    batch = batch_for_shader(shader, 'TRIS', {"pos": [p1, p2, p3]})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)
    
    draw_polyline([p2, p1, p3], border_color, border_width, viewport_size)

# --- TEXT WRAPPING ---
def wrap_text(text, max_width, font_id=0, font_size=14):
    blf.size(font_id, font_size)
    paragraphs = text.split('\n')
    lines = []
    for para in paragraphs:
        if not para:
            lines.append("")
            continue
        words = para.split(' ')
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word]) if current_line else word
            w, h = blf.dimensions(font_id, test_line)
            if w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        if current_line:
            lines.append(' '.join(current_line))
    return lines

# --- GEOMETRY GENERATOR ---
def get_paperclip_path(cx, cy, s):
    points = []
    
    def add_arc(acx, acy, r, start, end, steps=12):
        for i in range(steps + 1):
            a = start + (end - start) * (i / steps)
            points.append((acx + math.cos(a) * r, acy + math.sin(a) * r))

    points.append((cx + 4*s, cy + 10*s))
    points.append((cx + 4*s, cy - 10*s))
    add_arc(cx, cy - 10*s, 4*s, 0.0, -math.pi, steps=10)
    points.append((cx - 4*s, cy + 22*s))
    add_arc(cx + 4*s, cy + 22*s, 8*s, math.pi, 0.0, steps=10)
    points.append((cx + 12*s, cy - 25*s))
    add_arc(cx, cy - 25*s, 12*s, 0.0, -math.pi, steps=10)
    points.append((cx - 12*s, cy + 5*s))
    
    return points

def rotate_points(points, cx, cy, angle):
    if angle == 0.0:
        return points
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    rotated = []
    for px, py in points:
        dx = px - cx
        dy = py - cy
        rx = cx + dx * cos_a - dy * sin_a
        ry = cy + dx * sin_a + dy * cos_a
        rotated.append((rx, ry))
    return rotated

# --- CLIPPER STATE ---
class ClipperState:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.viewport_size = (100, 100)
        self.mouse_pos = (0, 0)
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.click_start_time = 0.0
        self.click_start_pos = (0, 0)
        
        # Animations
        self.blink_timer = 0.0
        self.is_blinking = False
        self.blink_duration = 0.16
        self.next_blink_time = time.time() + random.uniform(3.0, 6.0)
        self.blink_end_time = 0.0
        
        self.nod_start_time = 0.0
        self.jump_start_time = 0.0
        self.rotation = 0.0
        
        # Talking & Expression
        self.expression = 'HAPPY'
        self.is_talking = False
        
        # Speech Bubble
        self.bubble_visible = False
        self.bubble_text_target = ""
        self.bubble_char_count = 0
        self.bubble_lines = []
        self.last_char_time = 0.0
        self.bubble_buttons = []
        
        # Context Menu
        self.menu_visible = False
        self.menu_x = 0
        self.menu_y = 0
        self.menu_items = []
        self.menu_hover_idx = -1
        self.menu_scroll_offset = 0
        self.language = 'EN'
        
        # Tutorial State
        self.active_tutorial = None
        self.tutorial_step_idx = 0

# --- VIEWPORT DRAW CALLBACK ---
def draw_callback(op, context):
    try:
        if not op or not hasattr(op, 'state') or op.state is None:
            return
        state = op.state
        if not context or not hasattr(context, 'region') or context.region is None:
            return
        if not hasattr(context, 'area') or context.area is None or context.area.type != 'VIEW_3D':
            return
            
        state.viewport_size = (context.region.width, context.region.height)
        s = 1.5 # Scale factor
        
        now = time.time()
        
        # 1. Typing bubble effect
        if state.bubble_visible and state.bubble_text_target:
            if state.bubble_char_count < len(state.bubble_text_target):
                if now - state.last_char_time > 0.015:
                    chars_to_add = int((now - state.last_char_time) / 0.015)
                    if chars_to_add > 0:
                        state.bubble_char_count = min(state.bubble_char_count + chars_to_add, len(state.bubble_text_target))
                        state.last_char_time = now
                    state.is_talking = True
            else:
                if state.is_talking:
                    state.is_talking = False
                    
        # 2. Blinking eye effect
        if now > state.next_blink_time:
            state.is_blinking = True
            state.next_blink_time = now + random.uniform(3.5, 6.5)
            state.blink_end_time = now + state.blink_duration
        if state.is_blinking and now > state.blink_end_time:
            state.is_blinking = False
            
        # 3. Real-time state check for tutorials
        if state.active_tutorial and not state.is_talking:
            step = state.active_tutorial['steps'][state.tutorial_step_idx]
            check_func = step.get('check')
            if check_func:
                if safe_check_step(check_func, context):
                    op.next_tutorial_step()
                    
        # Calculate animations offsets
        breath_offset = 1.5 * math.sin(time.time() * 2.0) * s
        nod_offset = 0.0
        jump_offset = 0.0
        
        if state.nod_start_time > 0.0:
            t = time.time() - state.nod_start_time
            if t < 0.4:
                nod_offset = 6.0 * math.sin(t * 30.0) * s
            else:
                state.nod_start_time = 0.0
                
        if state.jump_start_time > 0.0:
            t = time.time() - state.jump_start_time
            duration = 0.6
            if t < duration:
                progress = t / duration
                jump_offset = 30.0 * math.sin(progress * math.pi) * s
                state.rotation = progress * 2.0 * math.pi
            else:
                state.jump_start_time = 0.0
                state.rotation = 0.0
                
        dcx = state.x
        dcy = state.y + breath_offset + nod_offset + jump_offset
        
        # 1. Shadow of paperclip body
        shadow_points = get_paperclip_path(dcx + 2*s, dcy - 2*s, s)
        shadow_points = rotate_points(shadow_points, dcx, dcy, state.rotation)
        draw_polyline(shadow_points, (0.0, 0.0, 0.0, 0.22), 8.0*s, state.viewport_size)
        
        # 2. Border of paperclip body
        border_points = get_paperclip_path(dcx, dcy, s)
        border_points = rotate_points(border_points, dcx, dcy, state.rotation)
        draw_polyline(border_points, (0.2, 0.2, 0.23, 1.0), 6.5*s, state.viewport_size)
        
        # 3. Main paperclip body (metallic silver)
        draw_polyline(border_points, (0.83, 0.84, 0.86, 1.0), 4.0*s, state.viewport_size)
        draw_polyline(border_points, (0.95, 0.95, 0.97, 1.0), 1.2*s, state.viewport_size)
        
        # 4. Eyes & Pupils
        lex_orig, ley_orig = dcx - 7.5*s, dcy + 13*s
        rex_orig, rey_orig = dcx + 7.5*s, dcy + 13*s
        
        rotated_eyes = rotate_points([(lex_orig, ley_orig), (rex_orig, rey_orig)], dcx, dcy, state.rotation)
        lex, ley = rotated_eyes[0]
        rex, rey = rotated_eyes[1]
        
        eye_r = 7.0*s
        
        if state.is_blinking:
            lid_y_l = ley - 1*s
            lid_y_r = rey - 1*s
            draw_polyline([(lex - 6*s, lid_y_l + 1*s), (lex, lid_y_l - 1*s), (lex + 6*s, lid_y_l + 1*s)], (0.1, 0.1, 0.1, 1.0), 2.5*s, state.viewport_size)
            draw_polyline([(rex - 6*s, lid_y_r + 1*s), (rex, lid_y_r - 1*s), (rex + 6*s, lid_y_r + 1*s)], (0.1, 0.1, 0.1, 1.0), 2.5*s, state.viewport_size)
        else:
            draw_circle(lex, ley, eye_r, (1.0, 1.0, 1.0, 1.0))
            draw_circle(rex, rey, eye_r, (1.0, 1.0, 1.0, 1.0))
            
            draw_circle_outline(lex, ley, eye_r, (0.1, 0.1, 0.1, 1.0), 1.5*s, state.viewport_size)
            draw_circle_outline(rex, rey, eye_r, (0.1, 0.1, 0.1, 1.0), 1.5*s, state.viewport_size)
            
            pupil_r = 2.8*s
            limit = eye_r - pupil_r - 0.5*s
            
            ldx, ldy = state.mouse_pos[0] - lex, state.mouse_pos[1] - ley
            ldist = math.hypot(ldx, ldy)
            if ldist > 0:
                lf = min(ldist * 0.03, limit)
                lex_p = lex + (ldx / ldist) * lf
                ley_p = ley + (ldy / ldist) * lf
            else:
                lex_p, ley_p = lex, ley
                
            rdx, rdy = state.mouse_pos[0] - rex, state.mouse_pos[1] - rey
            rdist = math.hypot(rdx, rdy)
            if rdist > 0:
                rf = min(rdist * 0.03, limit)
                rex_p = rex + (rdx / rdist) * rf
                rey_p = rey + (rdy / rdist) * rf
            else:
                rex_p, rey_p = rex, rey
                
            draw_circle(lex_p, ley_p, pupil_r, (0.08, 0.08, 0.08, 1.0))
            draw_circle(rex_p, rey_p, pupil_r, (0.08, 0.08, 0.08, 1.0))
            
            draw_circle(lex_p + 1.0*s, ley_p + 1.0*s, 0.8*s, (1.0, 1.0, 1.0, 1.0))
            draw_circle(rex_p + 1.0*s, rey_p + 1.0*s, 0.8*s, (1.0, 1.0, 1.0, 1.0))
            
        # 5. Eyebrows
        eb_y_l_orig = dcy + 21*s
        eb_y_r_orig = dcy + 21*s
        eb_h_l_orig = 0
        eb_h_r_orig = 0
        
        if state.expression == 'THINKING':
            eb_y_l_orig = dcy + 19*s
            eb_y_r_orig = dcy + 23*s
            eb_h_l_orig = 1.8*s
            eb_h_r_orig = -1.8*s
        elif state.is_talking:
            osc = math.sin(time.time() * 20) * 0.8 * s
            eb_y_l_orig += osc
            eb_y_r_orig += osc
            
        eb_l_pts = rotate_points([(lex_orig - 7*s, eb_y_l_orig - eb_h_l_orig), (lex_orig + 4*s, eb_y_l_orig + eb_h_l_orig)], dcx, dcy, state.rotation)
        eb_r_pts = rotate_points([(rex_orig - 4*s, eb_y_r_orig + eb_h_r_orig), (rex_orig + 7*s, eb_y_r_orig - eb_h_r_orig)], dcx, dcy, state.rotation)
        
        draw_polyline(eb_l_pts, (0.1, 0.1, 0.12, 1.0), 2.2*s, state.viewport_size)
        draw_polyline(eb_r_pts, (0.1, 0.1, 0.12, 1.0), 2.2*s, state.viewport_size)
        
        # 6. Mouth
        mx_c_orig, my_c_orig = dcx, dcy - 1.5*s
        mx_c, my_c = rotate_points([(mx_c_orig, my_c_orig)], dcx, dcy, state.rotation)[0]
        
        if state.is_talking:
            draw_circle(mx_c, my_c, 3.2*s, (0.1, 0.1, 0.1, 1.0))
            draw_circle(mx_c, my_c - 1.3*s, 1.8*s, (0.9, 0.38, 0.45, 1.0))
        elif state.expression == 'THINKING':
            m_pts = rotate_points([(mx_c_orig - 4*s, my_c_orig), (mx_c_orig, my_c_orig - 1.0*s), (mx_c_orig + 4*s, my_c_orig)], dcx, dcy, state.rotation)
            draw_polyline(m_pts, (0.1, 0.1, 0.1, 1.0), 2.0*s, state.viewport_size)
        else:
            m_pts = [
                (mx_c_orig - 4.5*s, my_c_orig + 1*s),
                (mx_c_orig - 2*s, my_c_orig - 2*s),
                (mx_c_orig, my_c_orig - 3.0*s),
                (mx_c_orig + 2*s, my_c_orig - 2*s),
                (mx_c_orig + 4.5*s, my_c_orig + 1*s)
            ]
            m_pts = rotate_points(m_pts, dcx, dcy, state.rotation)
            draw_polyline(m_pts, (0.1, 0.1, 0.1, 1.0), 2.2*s, state.viewport_size)

        # 7. Draw Speech Bubble
        draw_speech_bubble(dcx, dcy, s, state, context)
        
        # 8. Draw Context Menu
        draw_context_menu(state)
        
        if (state.is_talking or 
            state.is_blinking or 
            state.nod_start_time > 0.0 or 
            state.jump_start_time > 0.0 or 
            state.is_dragging):
            safe_tag_redraw(context)
    except Exception:
        pass

# --- DRAWING BUBBLE AND MENU ---
def draw_speech_bubble(cx, cy, s, state, context):
    try:
        if not state.bubble_visible or not state.bubble_text_target:
            return
            
        font_id = 0
        font_size = int(12 * s)
        blf.size(font_id, font_size)
        
        max_w = int(185 * s)
        line_h = int(16 * s)
        padding = int(12 * s)
        
        current_text = state.bubble_text_target[:state.bubble_char_count]
        lines = wrap_text(current_text, max_w, font_id, font_size)
        state.bubble_lines = lines
        
        if not lines:
            return
            
        text_h = len(lines) * line_h
        button_area_h = int(32 * s) if state.bubble_buttons else 0
        
        bw = max_w + padding * 2
        bh = text_h + padding * 2 + button_area_h
        
        is_left = cx > state.viewport_size[0] - 280
        
        if is_left:
            bx = cx - bw - 30*s
            by = cy + 5*s
            px, py = cx - 12*s, cy + 10*s
        else:
            bx = cx + 30*s
            by = cy + 5*s
            px, py = cx + 12*s, cy + 10*s
            
        draw_rounded_rect(bx + 2.5*s, by - 2.5*s, bw, bh, 8*s, (0.0, 0.0, 0.0, 0.14))
        bg_color = (1.0, 1.0, 0.88, 1.0)
        draw_rounded_rect(bx, by, bw, bh, 8*s, bg_color)
        draw_bubble_pointer(bx, by, px, py, is_left, bw, bg_color, (0.12, 0.12, 0.15, 1.0), 1.5*s, state.viewport_size)
        draw_rounded_rect_outline(bx, by, bw, bh, 8*s, (0.12, 0.12, 0.15, 1.0), 1.5*s, state.viewport_size)
        
        blf.color(font_id, 0.08, 0.08, 0.1, 1.0)
        for i, line in enumerate(lines):
            lx = bx + padding
            ly = by + bh - padding - (i + 1) * line_h + int(1.5 * s)
            blf.position(font_id, lx, ly, 0)
            blf.draw(font_id, line)
            
        if state.bubble_buttons:
            btn_count = len(state.bubble_buttons)
            btn_w = int((bw - padding * 2 - (btn_count - 1) * 8 * s) / btn_count)
            btn_h = int(22 * s)
            btn_y = by + padding
            
            for idx, btn in enumerate(state.bubble_buttons):
                btn_x = bx + padding + idx * (btn_w + int(8 * s))
                btn['rect'] = (btn_x, btn_y, btn_w, btn_h)
                
                mx, my = state.mouse_pos
                is_hover = (btn_x <= mx <= btn_x + btn_w) and (btn_y <= my <= btn_y + btn_h)
                
                if btn.get('type') == 'next':
                    bg = (0.2, 0.52, 0.33, 1.0) if not is_hover else (0.24, 0.62, 0.4, 1.0)
                    tc = (1.0, 1.0, 1.0, 1.0)
                elif btn.get('type') == 'exit':
                    bg = (0.7, 0.22, 0.22, 1.0) if not is_hover else (0.8, 0.28, 0.28, 1.0)
                    tc = (1.0, 1.0, 1.0, 1.0)
                else:
                    bg = (0.83, 0.83, 0.85, 1.0) if not is_hover else (0.88, 0.88, 0.9, 1.0)
                    tc = (0.1, 0.1, 0.12, 1.0)
                    
                draw_rounded_rect(btn_x, btn_y, btn_w, btn_h, 4*s, bg)
                draw_rounded_rect_outline(btn_x, btn_y, btn_w, btn_h, 4*s, (0.12, 0.12, 0.15, 1.0), 1.0*s, state.viewport_size)
                
                blf.size(font_id, int(11 * s))
                tw, th = blf.dimensions(font_id, btn['text'])
                tx = btn_x + (btn_w - tw) / 2
                ty = btn_y + (btn_h - th) / 2 + int(1 * s)
                blf.color(font_id, *tc)
                blf.position(font_id, tx, ty, 0)
                blf.draw(font_id, btn['text'])
    except Exception:
        pass

def get_context_menu_bounds(state):
    try:
        s = 1.5
        font_id = 0
        font_size = int(11 * s)
        blf.size(font_id, font_size)
        
        max_tw = int(150 * s)
        for item in state.menu_items:
            tw, th = blf.dimensions(font_id, item['text'])
            if tw > max_tw:
                max_tw = tw
                
        padding = int(5 * s)
        menu_w = int(max_tw + 34 * s)
        
        item_h = int(24 * s)
        max_visible = 10
        num_visible = min(len(state.menu_items), max_visible)
        menu_h = num_visible * item_h + padding * 2
        
        vw, vh = state.viewport_size
        mx, my = state.menu_x, state.menu_y
        
        if mx + menu_w > vw - 10:
            x = max(10, mx - menu_w)
        else:
            x = max(10, mx)
        x = min(vw - menu_w - 10, max(10, x))
            
        if my - menu_h < 10:
            y = min(vh - 10, my + menu_h)
        else:
            y = min(vh - 10, my)
        y = min(vh - 10, max(menu_h + 10, y))
            
        return x, y, menu_w, menu_h, item_h, padding, max_visible, num_visible
    except Exception:
        return 10, 10, 200, 200, 24, 5, 10, 5

def draw_context_menu(state):
    try:
        if not state.menu_visible or not state.menu_items:
            return
            
        s = 1.5
        font_id = 0
        font_size = int(11 * s)
        blf.size(font_id, font_size)
        
        x, y, menu_w, menu_h, item_h, padding, max_visible, num_visible = get_context_menu_bounds(state)
        items = state.menu_items
        total_items = len(items)
        
        max_scroll = max(0, total_items - max_visible)
        state.menu_scroll_offset = max(0, min(state.menu_scroll_offset, max_scroll))
        scroll = state.menu_scroll_offset
        
        draw_rounded_rect(x + 2.5*s, y - menu_h - 2.5*s, menu_w, menu_h, 6*s, (0.0, 0.0, 0.0, 0.22))
        bg_color = (0.11, 0.12, 0.14, 0.96)
        draw_rounded_rect(x, y - menu_h, menu_w, menu_h, 6*s, bg_color)
        draw_rounded_rect_outline(x, y - menu_h, menu_w, menu_h, 6*s, (0.28, 0.28, 0.32, 1.0), 1.0*s, state.viewport_size)
        
        visible_items = items[scroll : scroll + num_visible]
        
        if state.menu_hover_idx != -1:
            rel_idx = state.menu_hover_idx - scroll
            if 0 <= rel_idx < num_visible:
                hy = y - padding - (rel_idx + 1) * item_h
                draw_rounded_rect(x + int(2*s), hy + int(0.5*s), menu_w - int(10*s), item_h - int(1*s), 4*s, (0.18, 0.44, 0.75, 0.85))
                
        for rel_idx, item in enumerate(visible_items):
            abs_idx = scroll + rel_idx
            tx = x + int(10 * s)
            ty = y - padding - (rel_idx + 1) * item_h + int(5 * s)
            if abs_idx == state.menu_hover_idx:
                blf.color(font_id, 1.0, 1.0, 1.0, 1.0)
            else:
                blf.color(font_id, 0.84, 0.84, 0.87, 1.0)
            blf.position(font_id, tx, ty, 0)
            blf.draw(font_id, item['text'])
            
        if total_items > max_visible:
            bar_w = int(4 * s)
            bar_x = x + menu_w - bar_w - int(3 * s)
            track_h = menu_h - padding * 2
            thumb_h = max(int(16 * s), int(track_h * (max_visible / total_items)))
            thumb_y = y - padding - thumb_h - int((track_h - thumb_h) * (scroll / max_scroll))
            draw_rounded_rect(bar_x, thumb_y, bar_w, thumb_h, 2*s, (0.45, 0.48, 0.55, 0.8))
    except Exception:
        pass

# --- ACTIVE OPERATOR REFERENCE ---
_active_clipper_operator = None

# --- MODAL OPERATOR CLASS ---
class CLIPPER_OT_companion(bpy.types.Operator):
    bl_idname = "view3d.clipper_companion"
    bl_label = "Clipper Companion"
    
    should_exit = False
    
    def cancel_modal(self):
        self.should_exit = True

    def is_mouse_over_clipper(self, mx, my):
        try:
            dist = math.hypot(mx - self.state.x, my - self.state.y)
            return dist < (35.0 * 1.5)
        except Exception:
            return False
        
    def is_mouse_over_bubble(self, mx, my):
        try:
            if not self.state.bubble_visible or not self.state.bubble_lines:
                return False
            cx = self.state.x
            cy = self.state.y
            s = 1.5
            max_w = int(185 * s)
            line_h = int(16 * s)
            padding = int(12 * s)
            text_h = len(self.state.bubble_lines) * line_h
            button_area_h = int(32 * s) if self.state.bubble_buttons else 0
            bw = max_w + padding * 2
            bh = text_h + padding * 2 + button_area_h
            
            is_left = cx > self.state.viewport_size[0] - 280
            if is_left:
                bx = cx - bw - 30*s
            else:
                bx = cx + 30*s
            by = cy + 5*s
            return (bx <= mx <= bx + bw) and (by <= my <= by + bh)
        except Exception:
            return False

    def set_bubble_text(self, text):
        self.state.bubble_text_target = text
        self.state.bubble_char_count = 0
        self.state.bubble_lines = []
        self.state.last_char_time = time.time()
        self.state.is_talking = True

    def close_bubble(self):
        self.state.bubble_visible = False
        self.state.bubble_text_target = ""
        self.state.bubble_lines = []
        self.state.bubble_buttons = []
        self.state.is_talking = False

    def toggle_language(self):
        if self.state.language == 'EN':
            self.state.language = 'PL'
            msg = "Język został zmieniony na Polski! PL Wybierz samouczek z menu."
        else:
            self.state.language = 'EN'
            msg = "Language changed to English! GB Pick a tutorial from the menu."
        self.setup_context_menu()
        self.set_bubble_text(msg)
        self.state.expression = 'HAPPY'
        self.state.bubble_buttons = [
            {
                'text': 'Zamknij' if self.state.language == 'PL' else 'Close',
                'type': 'close',
                'action': lambda ctx: self.close_bubble()
            }
        ]
        self.state.bubble_visible = True
        self.trigger_nod()

    def show_random_tip(self):
        lang = self.state.language
        tips_list = TIPS.get(lang, TIPS['EN'])
        tip = random.choice(tips_list)
        self.state.expression = 'HAPPY'
        self.set_bubble_text(tip)
        self.state.bubble_buttons = [
            {
                'text': 'Zamknij' if lang == 'PL' else 'Close',
                'type': 'close',
                'action': lambda ctx: self.close_bubble()
            }
        ]
        self.state.bubble_visible = True

    def trigger_nod(self):
        self.state.nod_start_time = time.time()

    def trigger_celebrate(self):
        self.state.jump_start_time = time.time()

    def start_tutorial(self, tut_id):
        if tut_id in TUTORIALS:
            self.state.active_tutorial = TUTORIALS[tut_id]
            self.state.tutorial_step_idx = 0
            self.show_tutorial_step()
            self.trigger_nod()
            
    def show_tutorial_step(self):
        tut = self.state.active_tutorial
        lang = self.state.language
        step = tut['steps'][self.state.tutorial_step_idx]
        text_dict = step['text']
        text = text_dict.get(lang, text_dict.get('EN', ''))
        
        self.state.expression = 'THINKING' if step.get('check') else 'HAPPY'
        self.set_bubble_text(text)
        
        exit_lbl = "Wyjdź" if lang == 'PL' else "Exit"
        back_lbl = "Wstecz" if lang == 'PL' else "Back"
        is_last = self.state.tutorial_step_idx == len(tut['steps']) - 1
        next_lbl = ("Gotowe" if is_last else "Dalej") if lang == 'PL' else ("Done" if is_last else "Next")
        
        buttons = [
            {
                'text': exit_lbl,
                'type': 'exit',
                'action': lambda ctx: self.exit_tutorial()
            }
        ]
        if self.state.tutorial_step_idx > 0:
            buttons.append({
                'text': back_lbl,
                'type': 'back',
                'action': lambda ctx: self.prev_tutorial_step()
            })
            
        buttons.append({
            'text': next_lbl,
            'type': 'next',
            'action': lambda ctx: self.next_tutorial_step()
        })
        self.state.bubble_buttons = buttons
        self.state.bubble_visible = True

    def prev_tutorial_step(self):
        if self.state.tutorial_step_idx > 0:
            self.state.tutorial_step_idx -= 1
            self.show_tutorial_step()
            self.trigger_nod()
            
    def next_tutorial_step(self):
        tut = self.state.active_tutorial
        if self.state.tutorial_step_idx < len(tut['steps']) - 1:
            self.state.tutorial_step_idx += 1
            self.show_tutorial_step()
            self.trigger_nod()
        else:
            self.exit_tutorial()
            self.trigger_celebrate()
            
    def exit_tutorial(self):
        self.state.active_tutorial = None
        self.state.tutorial_step_idx = 0
        self.close_bubble()

    def setup_context_menu(self):
        lang = self.state.language
        if lang == 'PL':
            self.state.menu_items = [
                # Podstawowe
                {'text': "🎓 Samouczek: Wprowadzenie", 'action': lambda ctx: self.start_tutorial("intro")},
                {'text': "🛋️ Samouczek: Poduszka", 'action': lambda ctx: self.start_tutorial("cushion")},
                {'text': "💡 Samouczek: Światło i Kamera", 'action': lambda ctx: self.start_tutorial("lighting")},
                {'text': "🎨 Samouczek: Materiały", 'action': lambda ctx: self.start_tutorial("materials")},
                {'text': "✂️ Samouczek: Inset & Extrude", 'action': lambda ctx: self.start_tutorial("extrude")},
                {'text': "🗿 Samouczek: Rzeźbienie", 'action': lambda ctx: self.start_tutorial("sculpting")},
                {'text': "🔧 Samouczek: Subdivision", 'action': lambda ctx: self.start_tutorial("modifiers")},
                {'text': "🎬 Samouczek: Animacja", 'action': lambda ctx: self.start_tutorial("animation")},
                {'text': "🗺️ Samouczek: Rozwijanie UV", 'action': lambda ctx: self.start_tutorial("uv_unwrap")},
                {'text': "🌐 Samouczek: Węzły Shadera", 'action': lambda ctx: self.start_tutorial("nodes")},
                {'text': "👗 Samouczek: Symulacja Tkaniny", 'action': lambda ctx: self.start_tutorial("cloth")},
                {'text': "✨ Samouczek: Cząsteczki", 'action': lambda ctx: self.start_tutorial("particles")},
                {'text': "✏️ Samouczek: 2D Grease Pencil", 'action': lambda ctx: self.start_tutorial("grease_pencil")},
                {'text': "🎲 Samouczek: Ciała Sztywne", 'action': lambda ctx: self.start_tutorial("rigid_body")},
                {'text': "📐 Samouczek: Modyfikator Bevel", 'action': lambda ctx: self.start_tutorial("bevel_modifier")},
                # Zaawansowane
                {'text': "⚡ Samouczek: Geometry Nodes", 'action': lambda ctx: self.start_tutorial("geom_nodes")},
                {'text': "⚡ Samouczek: Advanced Hard Surface", 'action': lambda ctx: self.start_tutorial("hard_surface")},
                {'text': "⚡ Samouczek: Drivers & Automatyzacja", 'action': lambda ctx: self.start_tutorial("drivers")},
                {'text': "⚡ Samouczek: Rigging & Kinematyka IK", 'action': lambda ctx: self.start_tutorial("rigging_ik")},
                {'text': "⚡ Samouczek: Render Cycles & AgX", 'action': lambda ctx: self.start_tutorial("cycles_opt")},
                {'text': "⚡ Samouczek: Voxel Remesh & Dyntopo", 'action': lambda ctx: self.start_tutorial("sculpt_remesh")},
                {'text': "⚡ Samouczek: Shape Keys & Morfing", 'action': lambda ctx: self.start_tutorial("shape_keys")},
                {'text': "⚡ Samouczek: Krzywe Graph Editor", 'action': lambda ctx: self.start_tutorial("graph_editor")},
                {'text': "⚡ Samouczek: Wypalanie Tekstur (Baking)", 'action': lambda ctx: self.start_tutorial("baking_maps")},
                {'text': "⚡ Samouczek: Animacja NLA", 'action': lambda ctx: self.start_tutorial("nla_animation")},
                # Narzędzia
                {'text': "💡 Zapytaj o Wskazówkę", 'action': lambda ctx: self.show_random_tip()},
                {'text': "PL Język: Polski (Zmień na GB)", 'action': lambda ctx: self.toggle_language()},
                {'text': "📍 Zresetuj Pozycję", 'action': lambda ctx: self.reset_position()},
                {'text': "❌ Ukryj Clippera", 'action': lambda ctx: self.cancel_modal()}
            ]
        else:
            self.state.menu_items = [
                # Basics
                {'text': "🎓 Tutorial: Intro to Blender", 'action': lambda ctx: self.start_tutorial("intro")},
                {'text': "🛋️ Tutorial: Cushion Model", 'action': lambda ctx: self.start_tutorial("cushion")},
                {'text': "💡 Tutorial: Lighting & Camera", 'action': lambda ctx: self.start_tutorial("lighting")},
                {'text': "🎨 Tutorial: Materials & Shading", 'action': lambda ctx: self.start_tutorial("materials")},
                {'text': "✂️ Tutorial: Inset & Extrude", 'action': lambda ctx: self.start_tutorial("extrude")},
                {'text': "🗿 Tutorial: Sculpting Basics", 'action': lambda ctx: self.start_tutorial("sculpting")},
                {'text': "🔧 Tutorial: Subdivision Surface", 'action': lambda ctx: self.start_tutorial("modifiers")},
                {'text': "🎬 Tutorial: Keyframe Animation", 'action': lambda ctx: self.start_tutorial("animation")},
                {'text': "🗺️ Tutorial: UV Unwrapping", 'action': lambda ctx: self.start_tutorial("uv_unwrap")},
                {'text': "🌐 Tutorial: Shader Nodes", 'action': lambda ctx: self.start_tutorial("nodes")},
                {'text': "👗 Tutorial: Cloth Simulation", 'action': lambda ctx: self.start_tutorial("cloth")},
                {'text': "✨ Tutorial: Particle System", 'action': lambda ctx: self.start_tutorial("particles")},
                {'text': "✏️ Tutorial: 2D Grease Pencil", 'action': lambda ctx: self.start_tutorial("grease_pencil")},
                {'text': "🎲 Tutorial: Rigid Body Physics", 'action': lambda ctx: self.start_tutorial("rigid_body")},
                {'text': "📐 Tutorial: Bevel Modifier", 'action': lambda ctx: self.start_tutorial("bevel_modifier")},
                # Advanced
                {'text': "⚡ Tutorial: Geometry Nodes", 'action': lambda ctx: self.start_tutorial("geom_nodes")},
                {'text': "⚡ Tutorial: Advanced Hard Surface", 'action': lambda ctx: self.start_tutorial("hard_surface")},
                {'text': "⚡ Tutorial: Drivers & Automation", 'action': lambda ctx: self.start_tutorial("drivers")},
                {'text': "⚡ Tutorial: Rigging & IK", 'action': lambda ctx: self.start_tutorial("rigging_ik")},
                {'text': "⚡ Tutorial: Cycles Render & AgX", 'action': lambda ctx: self.start_tutorial("cycles_opt")},
                {'text': "⚡ Tutorial: Voxel Remesh & Dyntopo", 'action': lambda ctx: self.start_tutorial("sculpt_remesh")},
                {'text': "⚡ Tutorial: Shape Keys & Morphing", 'action': lambda ctx: self.start_tutorial("shape_keys")},
                {'text': "⚡ Tutorial: Graph Editor Curves", 'action': lambda ctx: self.start_tutorial("graph_editor")},
                {'text': "⚡ Tutorial: Texture Baking (Maps)", 'action': lambda ctx: self.start_tutorial("baking_maps")},
                {'text': "⚡ Tutorial: Non-Linear Animation (NLA)", 'action': lambda ctx: self.start_tutorial("nla_animation")},
                # Tools
                {'text': "💡 Ask for a Tip", 'action': lambda ctx: self.show_random_tip()},
                {'text': "GB Language: English (Switch to PL)", 'action': lambda ctx: self.toggle_language()},
                {'text': "📍 Reset Position", 'action': lambda ctx: self.reset_position()},
                {'text': "❌ Hide Clipper", 'action': lambda ctx: self.cancel_modal()}
            ]

    def reset_position(self):
        self.state.x = self.state.viewport_size[0] - 120
        self.state.y = 110
        self.trigger_nod()

    # --- MODAL SYSTEM ENGINES ---
    def invoke(self, context, event):
        global _active_clipper_operator
        
        if _active_clipper_operator is not None:
            _active_clipper_operator.cancel_modal()
            _active_clipper_operator = None
            try:
                context.window_manager.clipper_running = False
            except Exception:
                pass
            safe_tag_redraw(context)
            return {'CANCELLED'}
            
        self.state = ClipperState()
        
        window_width = 800
        window_height = 600
        try:
            if hasattr(context, 'area') and context.area and hasattr(context.area, 'regions'):
                window_width = context.area.width
                window_height = context.area.height
                for r in context.area.regions:
                    if hasattr(r, 'type') and r.type == 'WINDOW':
                        window_width = r.width
                        window_height = r.height
                        break
        except Exception:
            pass
                
        self.state.x = max(50, window_width - 120)
        self.state.y = 110
        self.state.viewport_size = (window_width, window_height)
        self.setup_context_menu()
        
        self._handle = bpy.types.SpaceView3D.draw_handler_add(
            draw_callback, (self, context), 'WINDOW', 'POST_PIXEL'
        )
        
        self._timer = context.window_manager.event_timer_add(0.016, window=context.window)
        
        context.window_manager.modal_handler_add(self)
        context.window_manager.clipper_running = True
        _active_clipper_operator = self
        
        print(f"[Clipper] Operator Summoned! Region size: {window_width}x{window_height}, Clipper at ({self.state.x}, {self.state.y})")
        safe_tag_redraw(context)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        global _active_clipper_operator
        
        try:
            if self.should_exit:
                try:
                    if hasattr(self, '_timer') and self._timer:
                        context.window_manager.event_timer_remove(self._timer)
                except Exception:
                    pass
                try:
                    if hasattr(self, '_handle') and self._handle:
                        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
                except Exception:
                    pass
                try:
                    context.window_manager.clipper_running = False
                except Exception:
                    pass
                if _active_clipper_operator == self:
                    _active_clipper_operator = None
                safe_tag_redraw(context)
                return {'FINISHED'}
                
            if event.type == 'MOUSEMOVE':
                if hasattr(event, 'mouse_region_x') and hasattr(event, 'mouse_region_y'):
                    self.state.mouse_pos = (event.mouse_region_x, event.mouse_region_y)
                
            if event.type == 'TIMER':
                safe_tag_redraw(context)
                return {'RUNNING_MODAL'}
                
            mx = getattr(event, 'mouse_region_x', 0)
            my = getattr(event, 'mouse_region_y', 0)
            
            # 1. Hover & Scroll updates for context menu
            if self.state.menu_visible:
                x, y, menu_w, menu_h, item_h, padding, max_visible, num_visible = get_context_menu_bounds(self.state)
                
                within_menu_x = x <= mx <= x + menu_w
                within_menu_y = y - menu_h <= my <= y
                
                if within_menu_x and within_menu_y:
                    max_scroll = max(0, len(self.state.menu_items) - max_visible)
                    if event.type == 'WHEELUPMOUSE':
                        self.state.menu_scroll_offset = max(0, self.state.menu_scroll_offset - 1)
                        safe_tag_redraw(context)
                        return {'RUNNING_MODAL'}
                    elif event.type == 'WHEELDOWNMOUSE':
                        self.state.menu_scroll_offset = min(max_scroll, self.state.menu_scroll_offset + 1)
                        safe_tag_redraw(context)
                        return {'RUNNING_MODAL'}
                        
                    rel_idx = int((y - padding - my) / item_h)
                    if 0 <= rel_idx < num_visible:
                        self.state.menu_hover_idx = self.state.menu_scroll_offset + rel_idx
                    else:
                        self.state.menu_hover_idx = -1
                else:
                    self.state.menu_hover_idx = -1
                    
            # 2. Clicks on Context Menu
            if self.state.menu_visible:
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    if self.state.menu_hover_idx != -1:
                        self.state.menu_items[self.state.menu_hover_idx]['action'](context)
                    self.state.menu_visible = False
                    safe_tag_redraw(context)
                    return {'RUNNING_MODAL'}
                elif event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
                    self.state.menu_visible = False
                    safe_tag_redraw(context)
                    return {'RUNNING_MODAL'}
                    
            # 3. Clicks on Speech Bubble Buttons
            if self.state.bubble_visible and self.state.bubble_buttons:
                if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                    for btn in self.state.bubble_buttons:
                        if 'rect' in btn:
                            bx, by, bw, bh = btn['rect']
                            if bx <= mx <= bx + bw and by <= my <= by + bh:
                                btn['action'](context)
                                safe_tag_redraw(context)
                                return {'RUNNING_MODAL'}
                                
            # 4. Drag & Drop or Click (Tip) on Clipper himself
            if event.type == 'LEFTMOUSE':
                if event.value == 'PRESS':
                    over = self.is_mouse_over_clipper(mx, my)
                    self.state.menu_visible = False
                    
                    if over:
                        self.state.is_dragging = True
                        self.state.drag_offset_x = self.state.x - mx
                        self.state.drag_offset_y = self.state.y - my
                        self.state.click_start_time = time.time()
                        self.state.click_start_pos = (mx, my)
                        safe_tag_redraw(context)
                        return {'RUNNING_MODAL'}
                        
                elif event.value == 'RELEASE':
                    if self.state.is_dragging:
                        self.state.is_dragging = False
                        
                        dx = mx - self.state.click_start_pos[0]
                        dy = my - self.state.click_start_pos[1]
                        drag_dist = math.hypot(dx, dy)
                        duration = time.time() - self.state.click_start_time
                        
                        if drag_dist < 12.0 and duration < 0.45:
                            self.show_random_tip()
                        safe_tag_redraw(context)
                        return {'RUNNING_MODAL'}
                        
            elif event.type == 'MOUSEMOVE' and self.state.is_dragging:
                self.state.x = mx + self.state.drag_offset_x
                self.state.y = my + self.state.drag_offset_y
                
                window_width = self.state.viewport_size[0]
                window_height = self.state.viewport_size[1]
                if hasattr(context, 'area') and context.area and hasattr(context.area, 'regions'):
                    for r in context.area.regions:
                        if hasattr(r, 'type') and r.type == 'WINDOW':
                            window_width = r.width
                            window_height = r.height
                            break
                
                self.state.x = max(30, min(self.state.x, window_width - 30))
                self.state.y = max(40, min(self.state.y, window_height - 40))
                safe_tag_redraw(context)
                return {'RUNNING_MODAL'}
                
            # 5. Right Click on Clipper (opens context menu)
            if event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
                over = self.is_mouse_over_clipper(mx, my)
                if over:
                    self.state.menu_x = mx
                    self.state.menu_y = my
                    self.state.menu_visible = True
                    self.state.menu_scroll_offset = 0
                    self.state.bubble_visible = False
                    self.state.menu_hover_idx = -1
                    safe_tag_redraw(context)
                    return {'RUNNING_MODAL'}
                    
            # 6. Esc key cancels operator
            if event.type == 'ESC' and event.value == 'PRESS':
                self.cancel_modal()
                return {'RUNNING_MODAL'}
                
            if hasattr(context, 'window') and context.window:
                if self.is_mouse_over_clipper(mx, my):
                    try:
                        context.window.cursor_modal_set('HAND')
                    except Exception:
                        pass
                else:
                    try:
                        context.window.cursor_modal_restore()
                    except Exception:
                        pass
                
            if event.type in {'LEFTMOUSE', 'RIGHTMOUSE'} and self.is_mouse_over_bubble(mx, my):
                return {'RUNNING_MODAL'}
                
            return {'PASS_THROUGH'}
        except Exception as e:
            print(f"[Clipper] Modal Exception suppressed: {e}")
            return {'PASS_THROUGH'}

# --- SIDEBAR PANEL CLASS ---
class CLIPPER_PT_panel(bpy.types.Panel):
    bl_label = "Clipper Companion"
    bl_idname = "CLIPPER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Clipper'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        is_running = getattr(wm, "clipper_running", False)
        
        col = layout.column(align=True)
        col.scale_y = 1.3
        
        if not is_running:
            col.operator("view3d.clipper_companion", text="Summon Clipper", icon='USER')
        else:
            col.operator("view3d.clipper_companion", text="Dismiss Clipper", icon='PANEL_CLOSE')

# --- ADDON REGISTRATION ---
def register():
    bpy.utils.register_class(CLIPPER_OT_companion)
    bpy.utils.register_class(CLIPPER_PT_panel)
    bpy.types.WindowManager.clipper_running = bpy.props.BoolProperty(default=False)

def unregister():
    global _active_clipper_operator
    if _active_clipper_operator is not None:
        try:
            _active_clipper_operator.cancel_modal()
        except Exception:
            pass
        _active_clipper_operator = None
        
    bpy.utils.unregister_class(CLIPPER_PT_panel)
    bpy.utils.unregister_class(CLIPPER_OT_companion)
    try:
        del bpy.types.WindowManager.clipper_running
    except Exception:
        pass

if __name__ == "__main__":
    register()
