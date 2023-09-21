import requests
from bs4 import BeautifulSoup

# List of URLs
urls = [
    "https://hdtoday.tv/movie/watch-the-engineer-hd-99454",
    # Add more URLs here
]

# Specify the target class names
target_classes_col5 = [
    "heading-name",
    "btn btn-sm btn-radius btn-warning btn-imdb",
    "description",
    "col-xl-5 col-lg-6 col-md-8 col-sm-12",
]

target_classes_col6 = [
    "col-xl-6 col-lg-6 col-md-4 col-sm-12",
]

# Create an HTML file to save the output
with open("hdtoday.html", "w", encoding="utf-8") as html_file:
    html_file.write("<html><head><style>")
    html_file.write("table { border-collapse: collapse; width: 100%; }")
    html_file.write("td { padding: 10px; border: 1px solid #ddd; }")
    html_file.write(".col5 { background-color: #f2f2f2; }")
    html_file.write(".col6 { background-color: #e0e0e0; }")
    html_file.write("</style></head><body>")

    # Loop through each URL
    for url in urls:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Write the URL as a header
            html_file.write(f"<h1>URL: {url}</h1>")

            # Create a table for col-xl-5 content
            html_file.write("<table>")
            html_file.write("<colgroup><col class='col5'><col class='col5'></colgroup>")
            for class_name in target_classes_col5:
                div_tags = soup.find_all('div', class_=class_name)
                h2_tags = soup.find_all('h2', class_=class_name)
                button_tags = soup.find_all('button', class_=class_name)

                for tag in div_tags + h2_tags + button_tags:
                    tag_content = tag.get_text(strip=True)
                    if class_name == "heading-name":
                        class_name = "Movie Name"
                    elif class_name == "btn btn-sm btn-radius btn-warning btn-imdb":
                        class_name = "IMDB Rating"
                    elif class_name == "description":
                        class_name = "Movie Short Story"
                    html_file.write("<tr>")
                    html_file.write(f"<td class='col5'><strong>{class_name}</strong></td>")
                    html_file.write(f"<td class='col5'>{tag_content}</td>")
                    html_file.write("</tr>")
            html_file.write("</table>")

            col6_div = soup.find('div', class_='col-xl-6 col-lg-6 col-md-4 col-sm-12')
            if col6_div:
                # Create a table for col-xl-6 content
                html_file.write("<table>")
                html_file.write("<colgroup><col class='col6'><col class='col6'></colgroup>")
                row_lines = col6_div.find_all('div', class_='row-line')

                for row_line in row_lines:
                    type_element = row_line.find('span', class_='type')
                    strong_text = type_element.find('strong').text.strip()
                    if strong_text == "Released:":
                        strong_text = "Released"
                    content = row_line.get_text(strip=True).replace(strong_text, '', 1)
                    html_file.write("<tr>")
                    html_file.write(f"<td class='col6'><strong>{strong_text}</strong></td>")
                    html_file.write(f"<td class='col6'>{content}</td>")
                    html_file.write("</tr>")
                html_file.write("</table>")
            else:
                html_file.write("<p>Class 'col-xl-6 col-lg-6 col-md-4 col-sm-12' not found.</p>")

            html_file.write("<br>")
        else:
            html_file.write(f"<p>Failed to retrieve the webpage at URL: {url}</p>")

    html_file.write("</body></html>")

print("Data saved to 'hdtoday.html'")
