def return_template_name():
    keys = ['Marketing', 'Business', 'Real Estate', 'Professional', 'Rouge', 'Sunrise', 'Wellness', 'Science',
            'Executive',
            'Caption Grey', 'Black and White', 'Remote', 'Lemon', 'Facts and Figures', 'Metro', 'Metro Caption',
            'Investigate', 'Samaritan', 'Books', 'Lux', 'Home', 'Graceful', 'Unity', 'Strategy', 'Epicure', 'Saturate',
            'SketchMark', 'Florentine', 'Money', 'Slate', 'Print', 'Flashlight', 'Beach', 'Land', 'Earth', 'Natural',
            'Retro Boutique', 'Beauty', 'Tracer', 'Fun', 'Cosmic', 'Synth', 'Subtitle Standard', 'TechHead', 'Party',
            'Fashion', 'Bricks', 'Moonrise', 'Letter', 'Elegant', 'Standard', 'Caption Dark', 'Caption Highlight',
            'Caption Italics', 'Caption Thin', 'Caption Yellow', 'Caption Fade', 'Caption Subtitles', 'Travel',
            'Pictory',
            'Subtitle Default']

    # Create a dictionary to map numbers to keys
    key_mapping = {str(i): key for i, key in enumerate(keys, start=1)}

    while True:
        print("Choose a category:")
        for key_number, key_name in key_mapping.items():
            print(f"Press {key_number} for {key_name}")

        user_input = input("Enter your choice (or 'q' to quit): ")

        if user_input.lower() == 'q':
            break

        selected_key = key_mapping.get(user_input)

        if selected_key:
            print(f"You selected: {selected_key}")
            return selected_key
        else:
            print("Invalid choice. Please enter a valid number.")