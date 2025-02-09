import re
import os

def to_html(srt_file, output_html):
    with open(srt_file, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()

    extracted_lines = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip lines that are just numbers
        if line.isdigit():
            continue

        # Skip lines that are timestamps (formatted as "00:00:00,000 --> 00:00:00,000")
        if re.match(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", line):
            continue

        extracted_lines.append(line)

    # Write to HTML file
    with open(output_html, "w", encoding="utf-8") as file:
        file.write("<html>\n<head>\n<title>Extracted SRT Subtitles</title>\n</head>\n<body>\n")

        for line in extracted_lines:
            file.write(f"  <p class='subtitle'>{line}</p>\n")

        file.write("</body>\n</html>")


# TEST
# to_html("sub.srt", "output2.html")

# Convert all .srt files to HTML files
def convert_srt_files_in_directory(input_dir, output_dir):
    c = 0
    for filename in os.listdir(input_dir):
        # Check if the file is an .srt file
        if filename.endswith(".srt"):
            srt_file_path = os.path.join(input_dir, filename)

            # Generate the output HTML filename in the desired output directory
            name = "lang" + str(c)
            output_html_path = os.path.join(output_dir, f"{name}.html")
            c += 1

            # Convert the SRT to HTML
            to_html(srt_file_path, output_html_path)
            print(f"Converted {filename} to {output_html_path}")

input_directory = "script_srt"
output_directory = "script_html"
convert_srt_files_in_directory(input_directory, output_directory)
