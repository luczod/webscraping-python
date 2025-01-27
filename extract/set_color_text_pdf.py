import pikepdf

def change_text_color_to_white(input_pdf, output_pdf):
    """
    Changes the text color to white for text matching the pattern 'Tm\\n(text)Tj\\n1'
    in the content streams of a PDF.

    Args:
        input_pdf (str): Path to the input PDF file.
        output_pdf (str): Path to save the modified PDF.
    """
    try:
        # Open the PDF
        with pikepdf.Pdf.open(input_pdf) as pdf:
            for page in pdf.pages:
                # Handle both single stream and array of streams
                if '/Contents' in page:
                    contents = page['/Contents']
                    
                    # If the contents is an array, process each stream
                    if isinstance(contents, pikepdf.Array):
                        new_streams = []
                        for stream in contents:
                            stream_data = stream.read_bytes().decode('latin1')
                            modified_stream = change_text_color(stream_data)
                            new_streams.append(pikepdf.Stream(pdf, modified_stream.encode('latin1')))
                        
                        # Replace the original array with the modified streams
                        page['/Contents'] = pikepdf.Array(new_streams)
                    
                    # If the contents is a single stream, process it directly
                    else:
                        content_stream = contents.read_bytes().decode('latin1')
                        modified_stream = change_text_color(content_stream)
                        page['/Contents'] = pikepdf.Stream(pdf, modified_stream.encode('latin1'))

            # Save the modified PDF
            pdf.save(output_pdf)

        print(f"Text color changed to white and saved to {output_pdf}")
    
    except Exception as e:
        print(f"An error occurred: {e}")


def change_text_color(content_stream):
    """
    Changes the text color to white for text matching the pattern 'Tm\\n(text)Tj\\n1'.

    Args:
        content_stream (str): PDF content stream as a text string.

    Returns:
        str: Modified content stream with text color changed to white.
    """
    import re

    # Define the regex pattern to match 'Tm\n(text)Tj\n1'
    pattern = r'(Td\n\(text\))'

    # Replace the matched text to include the color operator for white (1 1 1 rg)
    # Insert "1 1 1 rg\n" right before the matching text.
    modified_content = re.sub(pattern, r'1 1 1 rg\n\1', content_stream)

    return modified_content


# Example usage
for x in range(1, 411, 100):
    input_pdf_path = "dir/input_filename.pdf"
    output_pdf_path = "dir/output_filename.pdf"
    change_text_color_to_white(input_pdf_path, output_pdf_path)

