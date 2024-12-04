from manimlib import * #using manim from 3blue1brown instead of the manim community edition!
import numpy as np
import json
import os


# basic definitions
def register_define_fonts():
    base_project_dir = "/home/pawan/Documents/olenepal/manimOLEN/"
    fonts_dir = os.path.join(base_project_dir, "fonts")
    
    font_paths = [
        os.path.join(fonts_dir, "Kanchan Regular.ttf"),
        os.path.join(fonts_dir, "Aakha 2011.ttf"),
        os.path.join(fonts_dir, "Laila-Regular.ttf"),
        os.path.join(fonts_dir, "NotoSerifTibetan-Regular.ttf"),
        os.path.join(fonts_dir, "NotoSansTirhuta-Regular.ttf")
    ]
    
    # Check and register fonts
    for font_path in font_paths:
        if not os.path.exists(font_path):
            print(f"Warning: Font file not found: {font_path}")
            continue
        
        try:
            manimpango.register_font(font_path)
            print(f"Successfully registered font: {font_path}")
        except Exception as e:
            print(f"Error registering font {font_path}: {e}")

    # Define fonts for different languages
    nepali_font = "Laila"
    tibetan_font = "Noto Serif Tibetan"
    english_font = "Serif"
    nepalbhasa_font = "Aakha"
    maithili_font = "Noto Sans Tirhuta"
    return nepali_font, tibetan_font, english_font, nepalbhasa_font, maithili_font

def degrees_to_manimPI(degrees):
    """
    Converts an angle in degrees to a Manim-compatible form using PI.
    
    Args:
        degrees (float): Angle in degrees.
        
    Returns:
        float: Angle in terms of `a * PI`, suitable for use in Manim.
    """
    prefactor = degrees/180  # Convert degrees to prefactor of PI
    return prefactor * PI

print(degrees_to_manimPI(30))

# verify font paths and register, define fonts
nepali_font, tibetan_font, english_font, nepalbhasa_font, maithili_font = register_define_fonts() 

# Define the language for subtitles
language = "english"
show_subtitle = True

# Construction of 60 degrees
class Draw60DegreesCompassFinal(Scene):
    def __init__(self, language=language, **kwargs):
        super().__init__(**kwargs)
        self.show_subtitles = show_subtitle  # Toggle subtitles on/off for production
        self.language = language  # Language for subtitles
        self.subtitles = self.load_subtitles(language)

    def load_subtitles(self, language):
        """Load subtitles from the specified language's JSON file."""
        subtitle_file = f"subtitles60/{language}.json"
        if not os.path.exists(subtitle_file):
            raise FileNotFoundError(f"Subtitle file {subtitle_file} not found!")
        with open(subtitle_file, 'r', encoding='utf-8') as file:
            return json.load(file)

  
    def add_subtitle(self, key, font_size=30, max_width_ratio=0.7):
        """Helper function to add and animate subtitles at the bottom of the screen."""
        if not self.show_subtitles:
            return None, None

        # Get subtitle text from the subtitles dictionary
        subtitle_text = self.subtitles.get(key, "")

        # Choose the font based on the language
        font = self.get_font_by_language()

        # Calculate the maximum width for the subtitle text
        max_width = FRAME_WIDTH * max_width_ratio

        # Break the subtitle into multiple lines if it exceeds max width
        words = subtitle_text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if MarkupText(test_line, font_size=font_size, font=font).get_width() > max_width:
                lines.append(current_line.strip())
                current_line = word
            else:
                current_line = test_line

        lines.append(current_line.strip())  # Add the last line

        # Create a VGroup to stack lines and center them
        subtitle_lines = VGroup(*[
            MarkupText(line, font_size=font_size, font=font).set_color(WHITE)
            for line in lines
        ])
        subtitle_lines.arrange(DOWN, center=True, aligned_edge=ORIGIN)

        # Position the subtitle group at the bottom center of the screen
        subtitle_lines.move_to(3*DOWN)

        # Display the subtitle with an animation
        self.play(Write(subtitle_lines))
        return subtitle_lines

    def remove_subtitle(self, subtitle):
        """Helper function to remove subtitles."""
        if subtitle:
            self.play(FadeOut(subtitle)) # fade out the subtitle

    def get_font_by_language(self):
        """Get the appropriate font based on the selected language."""
        # Choose the font based on the language
        if self.language == "nepali":
            font = nepali_font
        elif self.language == "tibetan":
            font = tibetan_font
        elif self.language == "nepalbhasa":
            font = nepalbhasa_font
        elif self.language == "maithili":
            font = maithili_font
        else:
            font = english_font  # Default to English if language is not specified
        return font

    def construct(self):
        label_font_size = 24

        # Grid background with adjusted position
        grid = NumberPlane().fade(0.8).shift(DOWN)  # Shift grid down for better alignment
        self.add(grid)

        # Step 1: Draw a line segment PQ
        subtitle = self.add_subtitle("step_1")
        line_width_param = 3
        line = Line(LEFT * line_width_param, RIGHT * line_width_param, color=TEAL).shift(DOWN)
        
        P = Dot(line.get_start(), color=BLUE)
        Q = Dot(line.get_end(), color=BLUE)
        P_label = Text("P", font_size=label_font_size).next_to(P, LEFT)
        Q_label = Text("Q", font_size=label_font_size).next_to(Q, RIGHT)

        self.play(ShowCreation(line), FadeIn(P), FadeIn(Q))
        self.play(Write(P_label), Write(Q_label))
        self.play(Indicate(P), Indicate(Q))
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 2: Set the compass width
        subtitle = self.add_subtitle("step_2")
        mid_point = (line.get_start()+line.get_end())/2
        midpoint_PQ = Dot(mid_point, color=ORANGE).scale(1.2)
        self.play(FadeIn(midpoint_PQ))
        self.play(Indicate(midpoint_PQ))
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 3: Draw the first arc
        subtitle = self.add_subtitle("step_3")
        compass_radius = Line(P.get_center(), midpoint_PQ.get_center(), color=RED)
        arc_radius = compass_radius.get_length()
        self.play(ShowCreation(compass_radius), run_time=1)

        arc = Arc(radius=arc_radius, start_angle=0.8 * PI, angle=-1.05 * PI, color=MAROON).shift(P.get_center())
        self.play(ShowCreation(arc), run_time=2)

        arc_touch_point = P.get_center() + np.array([arc_radius, 0, 0])
        A = Dot(arc_touch_point, color=BLUE)
        A_label = Text("A", font_size=label_font_size).next_to(A, UP + RIGHT)
        self.play(FadeIn(A), Write(A_label))
        self.play(Indicate(A))
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 4: Draw the second arc
        subtitle = self.add_subtitle("step_4")
        arc_from_A = Arc(radius=arc_radius, start_angle=0.8 * PI, angle=-PI / 3, color=PURPLE).shift(A.get_center())
        self.play(ShowCreation(arc_from_A), run_time=2)
        self.remove_subtitle(subtitle)

        # Step 5: Calculate point O
        subtitle = self.add_subtitle("step_5")
        PA_vector = A.get_center() - P.get_center()
        rotation_matrix = np.array([[np.cos(PI / 3), -np.sin(PI / 3)], [np.sin(PI / 3), np.cos(PI / 3)]])
        rotated_PA = np.dot(rotation_matrix, PA_vector[:2])
        O_position = P.get_center() + np.array([rotated_PA[0], rotated_PA[1], 0])
        O = Dot(O_position, color=ORANGE)
        O_label = Text("O", font_size=label_font_size).next_to(O, UP)
        self.play(FadeIn(O), Write(O_label))
        self.play(Indicate(O))
        self.wait(2)
        self.remove_subtitle(subtitle)

        # Step 6: Draw the angle line
        subtitle = self.add_subtitle("step_6")
        direction_vector = O_position - P.get_center()
        extended_end = O_position + direction_vector
        angle_line_extended = Line(P.get_center(), extended_end, color=YELLOW)
        self.play(ShowCreation(angle_line_extended), run_time=2)
        self.remove_subtitle(subtitle)

        # Step 7: Add angle arc and label
        subtitle = self.add_subtitle("step_7")
        angle_arc = Arc(radius=0.5, start_angle=0.4 * PI, angle=-PI / 2.2, color=GREEN).shift(P.get_center())
        self.play(ShowCreation(angle_arc), run_time=1)

        # Adjusting the angle label position further from the arc
        arc_midpoint = angle_arc.get_arc_center()
        label_offset = angle_arc.get_center() * -0.3 
        label_position = arc_midpoint + label_offset
        angle_label = Text("60°", font_size=label_font_size).move_to(label_position)
        self.play(Write(angle_label))
        self.remove_subtitle(subtitle)

        # Wait to finalize the scene
        self.wait(2)

# Construction of 120 degrees
class Draw120DegreesCompassFinal(Scene):
    def __init__(self, language=language, **kwargs):
        super().__init__(**kwargs)
        self.show_subtitles = show_subtitle  # Toggle subtitles on/off for production
        self.language = language  # Language for subtitles
        self.subtitles = self.load_subtitles(language)

    def load_subtitles(self, language):
        """Load subtitles from the specified language's JSON file."""
        subtitle_file = f"subtitles120/{language}.json"
        if not os.path.exists(subtitle_file):
            raise FileNotFoundError(f"Subtitle file {subtitle_file} not found!")
        with open(subtitle_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def add_subtitle(self, key, font_size=30, max_width_ratio=0.7):
        """Helper function to add and animate subtitles at the bottom of the screen."""
        if not self.show_subtitles:
            return None, None

        # Get subtitle text from the subtitles dictionary
        subtitle_text = self.subtitles.get(key, "")

        # Choose the font based on the language
        font = self.get_font_by_language()

        # Calculate the maximum width for the subtitle text
        max_width = FRAME_WIDTH * max_width_ratio

        # Break the subtitle into multiple lines if it exceeds max width
        words = subtitle_text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if MarkupText(test_line, font_size=font_size, font=font).get_width() > max_width:
                lines.append(current_line.strip())
                current_line = word
            else:
                current_line = test_line

        lines.append(current_line.strip())  # Add the last line

        # Create a VGroup to stack lines and center them
        subtitle_lines = VGroup(*[
            MarkupText(line, font_size=font_size, font=font).set_color(WHITE)
            for line in lines
        ])
        subtitle_lines.arrange(DOWN, center=True, aligned_edge=ORIGIN)

        # Position the subtitle group at the bottom center of the screen
        subtitle_lines.move_to(3*DOWN)

        # Display the subtitle with an animation
        self.play(Write(subtitle_lines))
        return subtitle_lines

    def remove_subtitle(self, subtitle):
        """Helper function to remove subtitles."""
        if subtitle:
            self.play(FadeOut(subtitle)) # fade out the subtitle

    def get_font_by_language(self):
        """Get the appropriate font based on the selected language."""
        if self.language == "nepali":
            font = nepali_font
        elif self.language == "tibetan":
            font = tibetan_font
        elif self.language == "nepalbhasa":
            font = nepalbhasa_font
        elif self.language == "maithili":
            font = maithili_font
        else:
            font = english_font  # Default to English if language is not specified
        return font

    def construct(self):
        label_font_size = 24

        # Grid background with adjusted position
        grid = NumberPlane().fade(0.8).shift(DOWN)  # Shift grid down for better alignment
        self.add(grid)

        # Step 1: Draw ray OA
        subtitle = self.add_subtitle("step_1")
        ray = Line(LEFT * 3, RIGHT * 3, color=TEAL, stroke_width=2).shift(DOWN)
        O = Dot(ray.get_left(), color=BLUE)
        A = Dot(ray.get_right(), color=BLUE)
        O_label = Text("O", font_size=label_font_size).next_to(O, LEFT)
        A_label = Text("A", font_size=label_font_size).next_to(A, RIGHT)

        self.play(ShowCreation(ray), FadeIn(O), FadeIn(A))
        self.play(Write(O_label), Write(A_label))
        self.play(Indicate(O), Indicate(A))
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 2: Draw an arc from O
        subtitle = self.add_subtitle("step_2")
        radius = 3
        arc = Arc(radius=radius, start_angle=PI, angle=-PI, color=MAROON).shift(O.get_center())
        P = Dot(O.get_center() + np.array([radius, 0, 0]), color=BLUE)
        P_label = Text("P", font_size=label_font_size).next_to(P, UP+RIGHT)

        self.play(ShowCreation(arc))
        self.play(FadeIn(P), Write(P_label))
        self.play(Indicate(P))
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 3: Draw an arc from P to intersect at Q
        subtitle = self.add_subtitle("step_3")
        Q_pos = P.get_center() + np.array([
            radius * np.cos(2 * PI / 3),
            radius * np.sin(2 * PI / 3),
            0
        ])
        arc_from_P = Arc(
            radius=radius,
            start_angle=0.8*PI,
            angle=-0.25*PI,
            color=PURPLE
        ).shift(P.get_center())
        Q = Dot(Q_pos, color=BLUE)
        Q_label = Text("Q", font_size=label_font_size).next_to(Q, DOWN)

        self.play(ShowCreation(arc_from_P), FadeIn(Q), Write(Q_label))
        self.play(Indicate(Q))
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 4: Draw an arc from Q to intersect at S
        subtitle = self.add_subtitle("step_4")
        S_pos = O.get_center() + np.array([
            radius * np.cos(2 * PI / 3),
            radius * np.sin(2 * PI / 3),
            0
        ])
        arc_from_Q = Arc(
            radius=radius,
            start_angle=(1.1)*PI,
            angle=-PI / 6,
            color=GREEN
        ).shift(Q.get_center())
        S = Dot(S_pos, color=BLUE)
        S_label = Text("S", font_size=label_font_size).next_to(S, LEFT)

        self.play(ShowCreation(arc_from_Q), FadeIn(S), Write(S_label))
        self.play(Indicate(S))
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 5: Draw and extend line OS
        subtitle = self.add_subtitle("step_5")
        OS_vector = S.get_center() - O.get_center()
        extended_point = S.get_center() + 1.5 * OS_vector
        OS_extended = Line(O.get_center(), extended_point, color=YELLOW)
        D = Dot(extended_point, color=BLUE)
        D_label = Text("D", font_size=label_font_size).next_to(D, RIGHT)

        self.play(ShowCreation(OS_extended), FadeIn(D), Write(D_label))
        angle_arc = Arc(radius=0.5, start_angle=0, angle=2 * PI / 3, color=GREEN).shift(O.get_center())
        self.play(ShowCreation(angle_arc))

        # Adjusting the angle label position further from the arc
        arc_midpoint = angle_arc.get_arc_center()
        label_offset = angle_arc.get_center() * -0.3 
        label_position = arc_midpoint + label_offset
        angle_label = Text("120°", font_size=label_font_size).move_to(label_position)
        self.play(Write(angle_label))
        self.remove_subtitle(subtitle)


# Construction of 30 degrees
class Draw30DegreesCompassFinal(Scene):
    def __init__(self, language=language, **kwargs):
        super().__init__(**kwargs)
        self.show_subtitles = show_subtitle  # Toggle subtitles on/off for production
        self.language = language  # Language for subtitles
        self.subtitles = self.load_subtitles(language)
        
        # Consistent color palette for geometric elements
        self.POINT_COLOR = BLUE
        self.CONSTRUCTION_COLOR = TEAL
        self.ARC_COLORS = [MAROON, PURPLE, WHITE]
        self.HIGHLIGHT_COLOR = GREEN

    @staticmethod
    def degrees_to_manimPI(degrees):
        """
        Converts an angle in degrees to a Manim-compatible form using PI.
        
        Args:
            degrees (float): Angle in degrees.
            
        Returns:
            float: Angle in terms of `a * PI`, suitable for use in Manim.
        """
        prefactor = Fraction(degrees, 180)  # Convert degrees to prefactor of PI
        return prefactor * PI

    def load_subtitles(self, language):
        """
        Load subtitles from the specified language's JSON file.
        
        Args:
            language (str): Language code for subtitles.
        
        Returns:
            dict: Loaded subtitle dictionary.
        Raises:
            FileNotFoundError: If subtitle file is missing.
        """
        # Note: You'll need to create this JSON file with your subtitle translations
        subtitle_file = f"subtitles30/{language}.json"
        if not os.path.exists(subtitle_file):
            print(f"Warning: Subtitle file {subtitle_file} not found! Using default text.")
            return {
                "step_1": "Start by drawing a line segment OA",
                "step_2": "Draw an arc from O with a specific radius",
                # Add other default subtitle texts here
                "step_7": "Measure the angle AOE. It is 30 degrees!"
            }
        
        with open(subtitle_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def add_subtitle(self, key, font_size=30, max_width_ratio=0.7):
        """Helper function to add and animate subtitles at the bottom of the screen."""
        if not self.show_subtitles:
            return None, None

        # Get subtitle text from the subtitles dictionary
        subtitle_text = self.subtitles.get(key, "")

        # Choose the font based on the language
        font = self.get_font_by_language()

        # Calculate the maximum width for the subtitle text
        max_width = FRAME_WIDTH * max_width_ratio

        # Break the subtitle into multiple lines if it exceeds max width
        words = subtitle_text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if MarkupText(test_line, font_size=font_size, font=font).get_width() > max_width:
                lines.append(current_line.strip())
                current_line = word
            else:
                current_line = test_line

        lines.append(current_line.strip())  # Add the last line

        # Create a VGroup to stack lines and center them
        subtitle_lines = VGroup(*[
            MarkupText(line, font_size=font_size, font=font).set_color(WHITE)
            for line in lines
        ])
        subtitle_lines.arrange(DOWN, center=True, aligned_edge=ORIGIN)

        # Position the subtitle group at the bottom center of the screen
        subtitle_lines.move_to(3*DOWN)

        # Display the subtitle with an animation
        self.play(Write(subtitle_lines))
        return subtitle_lines

    def remove_subtitle(self, subtitle):
        """Helper function to remove subtitles."""
        if subtitle:
            self.play(FadeOut(subtitle)) # fade out the subtitle

    def highlight_point(self, point, label=None):
        """
        Create a pulsing highlight effect for a point.
        
        Args:
            point (Dot): The point to highlight.
            label (Text, optional): Label associated with the point.
        
        Returns:
            Animation sequence for highlighting.
        """
        pulse = AnimationGroup(
            point.animate.scale(1.5).set_color(self.HIGHLIGHT_COLOR),
            point.animate.scale(1/1.5).set_color(self.POINT_COLOR)
        )
        
        if label:
            return AnimationGroup(
                Indicate(point),
                Indicate(label),
                pulse
            )
        return pulse

    def construct(self):      
        label_font_size = 24

        # Enhanced grid background with more subtle grid
        grid = NumberPlane(
            x_range=[-7, 7, 1], 
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 0.5,
                "stroke_opacity": 0.2
            }
        ).shift(DOWN)
        self.add(grid)

        # Step 1: Draw OA with enhanced point and label highlighting
        subtitle = self.add_subtitle("step_1")
        ray = Line(LEFT * 3, RIGHT * 3, color=self.CONSTRUCTION_COLOR, stroke_width=2).shift(DOWN)
        O = Dot(ray.get_left(), color=self.POINT_COLOR)
        A = Dot(ray.get_right(), color=self.POINT_COLOR)
        O_label = Text("O", font_size=label_font_size).next_to(O, LEFT)
        A_label = Text("A", font_size=label_font_size).next_to(A, RIGHT)

        self.play(ShowCreation(ray), FadeIn(O, A))
        self.play(Write(O_label), Write(A_label))
        self.play(self.highlight_point(O, O_label), self.highlight_point(A, A_label))
        
        # Add visual cues about the starting point
        center_highlight = Circle(
            radius=0.3, 
            color=self.HIGHLIGHT_COLOR, 
            fill_opacity=0.2
        ).move_to(O.get_center())
        self.play(ShowCreation(center_highlight))
        
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 2: Draw an arc from O to intersect OA at C
        subtitle = self.add_subtitle("step_2")
        radius = 3
        arc_O = Arc(radius=radius, start_angle=self.degrees_to_manimPI(75), angle=-self.degrees_to_manimPI(80), color=MAROON).shift(O.get_center())
        C = Dot(O.get_center() + np.array([radius, 0, 0]), color=self.POINT_COLOR)
        C_label = Text("C", font_size=label_font_size).next_to(C, UP+RIGHT)

        self.play(ShowCreation(arc_O))
        self.play(FadeIn(C), Write(C_label))
        self.play(self.highlight_point(C, C_label))
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 3: Draw an arc from C to intersect first arc at D
        subtitle = self.add_subtitle("step_3")
        D_pos = O.get_center() + np.array([
            radius * np.cos(self.degrees_to_manimPI(60)),  # x coordinate
            radius * np.sin(self.degrees_to_manimPI(60)),  # y coordinate
            0
        ])
        arc_from_C = Arc(
            radius=radius,
            start_angle=self.degrees_to_manimPI(130),
            angle=-self.degrees_to_manimPI(20),
            color=PURPLE
        ).shift(C.get_center())
        D = Dot(D_pos, color=self.POINT_COLOR)
        D_label = Text("D", font_size=label_font_size).next_to(D, UP)
        
        self.play(ShowCreation(arc_from_C))
        self.play(FadeIn(D), Write(D_label))
        self.play(self.highlight_point(D, D_label))
        self.wait(1)
        self.remove_subtitle(subtitle)

        # Step 4: Show the 60 degree angle DOC with dotted extended line
        subtitle = self.add_subtitle("step_4")
        
        # Calculate extended point beyond D
        OD_vector = D.get_center() - O.get_center()
        extended_point = O.get_center() + 1.5 * OD_vector

        # Create dotted line OD extended
        OD_extended = DashedLine(
            O.get_center(),
            extended_point,
            color=TEAL,
            dash_length=0.15,
            dashed_ratio=0.5
        )
        
        # Create the 60 degree angle arc
        angle_60 = Arc(
            radius=0.7,
            start_angle=self.degrees_to_manimPI(0),
            angle=self.degrees_to_manimPI(60),
            color=GREEN
        ).shift(O.get_center())
        
        # Add angle label
        angle_label = Text("60°", font_size=label_font_size).next_to(
            angle_60.point_from_proportion(0.5),
            RIGHT + UP,
            buff=0.1
        )
        
        # Draw extended dotted line and show angle
        self.play(ShowCreation(OD_extended))
        self.play(ShowCreation(angle_60), Write(angle_label))
        self.wait(1)
        self.remove_subtitle(subtitle)
        
        self.play(FadeOut(angle_label), run_time=2)
        self.wait(1)

        # Step 5: Draw arcs from C and D to intersect
        subtitle = self.add_subtitle("step_5")
        
        # Calculate position of point E (intersection point)
        E_pos = O.get_center() + np.array([
            radius * np.cos(PI/6),  # x coordinate
            radius * np.sin(PI/6),  # y coordinate
            0
        ])
        
        # First arc: centered at C 
        arc_C = Arc(
            radius=radius,
            start_angle=self.degrees_to_manimPI(75),
            angle=-self.degrees_to_manimPI(30),
            color=WHITE
        ).shift(C.get_center())

        # Second arc: centered at D
        arc_D = Arc(
            radius=radius,
            start_angle=self.degrees_to_manimPI(15),
            angle=-self.degrees_to_manimPI(30),
            color=WHITE
        ).shift(D.get_center())

        self.play(ShowCreation(arc_C))
        self.wait(1)
        self.play(ShowCreation(arc_D))
        self.wait(1)
        
        # Find the intersection point E
        E_pos = D.get_center() + np.array([
            radius,  # x coordinate 
            0,      # y coordinate
            0       # no 3d in our construction
        ])

        E = Dot(E_pos, color=RED)
        E_label = Text("E", font_size=label_font_size).next_to(E, (UP+RIGHT)/2)

        self.play(FadeIn(E), Write(E_label))
        self.play(self.highlight_point(E, E_label))
        self.wait(1)

        # Step 6: Draw line segment OE
        subtitle = self.add_subtitle("step_6")
        
        # Calculate extended point beyond E
        OE_vector = E.get_center() - O.get_center()
        extended_point = O.get_center() + 1.5 * OE_vector
        
        # Create dotted line OE extended
        OE_extended = DashedLine(
            O.get_center(),
            extended_point,
            color=WHITE,
            dash_length=0.15,
            dashed_ratio=0.5
        )
        self.play(ShowCreation(OE_extended))
        self.wait(1)
        
        self.remove_subtitle(subtitle)
        
        # Step 7: Measure ∡AOE with enhanced angle highlighting
        subtitle = self.add_subtitle("step_7")
        
        # Prepare for angle highlighting
        OA_line = Line(O.get_center(), A.get_center(), color=BLUE, stroke_width=3)
        OE_line = Line(O.get_center(), E.get_center(), color=BLUE, stroke_width=3)
        
        # Create the angle ∡AOE
        angle_AOE = Arc(
            radius=0.7,
            start_angle=self.degrees_to_manimPI(0),
            angle=self.degrees_to_manimPI(30),
            color=BLUE
        ).shift(O.get_center())
        
        # Add the angle label
        angle_AOE_label = Text("30°", font_size=label_font_size).next_to(
            angle_AOE.point_from_proportion(0.5),
            RIGHT,
            buff=0.1
        )
        
        # Animated highlighting sequence
        self.play(
            # Gradually draw lines from O to A and O to E
            ShowCreation(OA_line),
            ShowCreation(OE_line),
            # Simultaneously create the angle arc
            ShowCreation(angle_AOE),
            run_time=2
        )
        
        # Pulsing and indication of the angle
        self.play(
            # Highlight the angle arc
            #angle_AOE.animate.set_color(YELLOW).set_stroke(width=4),
            # Write the angle label
            Write(angle_AOE_label),
            # Add a pulsing effect to the lines
            OA_line.animate.set_color(GOLD),
            OE_line.animate.set_color(GOLD),
            angle_AOE.animate.set_color(GOLD),
            
            run_time=1.5
        )
        
        # Brief pause to emphasize the 30-degree angle
        self.wait(2)
        self.remove_subtitle(subtitle)
        
        # Final pause with a subtle zoom out to show full construction
        self.play(
            grid.animate.scale(1.2).set_opacity(0.5),
            run_time=2
        )
        self.wait(2)


#