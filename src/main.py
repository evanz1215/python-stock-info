import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from models.stock import Stock


def main():
    data = fetch_data()
    # You can further process `data` if needed
    print(data)


def fetch_data():
    # Initialize a UserAgent
    ua = UserAgent()
    headers = {"User-Agent": ua.random}

    # Define the URL
    url = "https://mops.twse.com.tw/mops/web/t05sr01_1"

    # Make a GET request to the URL
    response = requests.get(url, headers=headers)
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the form and its hidden inputs
    form = soup.find("form", {"name": "fm_t05sr01_1"})

    if form is None:
        print("Form not found")
        return None

    hidden_inputs = form.find_all("input", {"type": "hidden"})

    # Create a dictionary of hidden input names and values
    hidden_input_dict = {
        input_elem["name"]: input_elem.get("value", "") for input_elem in hidden_inputs
    }

    # Find the table containing the data
    table = soup.find("table", {"class": "hasBorder"})

    # Initialize headers and data_rows
    headers = []
    data_rows = []

    if table:
        for row in table.find_all("tr"):
            if "tblHead" in row.get("class", []):
                headers = [th.text.strip() for th in row.find_all("th")]
            else:
                for td in row.find_all("td"):
                    data_line = td.text.strip()

                    for i in range(len(headers)):
                        print(f"{headers[i]}={data_line[i]}")

                    stock = Stock(
                        data_line[0],
                        data_line[1],
                        data_line[2],
                        data_line[3],
                        data_line[4],
                    )

                    data_rows.append(stock)

                # data_rows.append([td.text.strip() for td in row.find_all("td")])

    # Print the headers and the number of rows
    print("Headers:", headers)
    print(f"Total rows: {len(data_rows)}")

    return hidden_input_dict, headers, data_rows


if __name__ == "__main__":
    main()
