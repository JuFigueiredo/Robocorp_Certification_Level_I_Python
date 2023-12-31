from robocorp.tasks import task
from robocorp import browser

from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF
from RPA.Robocorp.Vault import Vault

@task
def robot_spare_bin_python():
    """Insert the sales data for the week and export it as a PDF"""

    # browser.configure(
    #     slowmo=1000,
    # )

    open_intranet_website()
    log_in()
    download_excel_file()
    fill_form_with_excel_data()
    collect_results()
    export_as_pdf()
    log_out()

def open_intranet_website():
    """Navigate to the given URL"""
    browser.goto("https://robotsparebinindustries.com/")


def log_in():
    """Fills the login form and clicks the 'Log in' button"""
    page = browser.page()
    _secret = Vault().get_secret("mariasecret")

    USERNAME = _secret["username"]
    PASSWORD = _secret["password"]

    page.fill("#username",USERNAME)
    page.fill("#password",PASSWORD)
    page.click("button:text('Log in')")


def fill_and_submit_sales_forms(sales_rep):
    """Fills in the sales data and click the 'Submit' button"""
    page = browser.page()

    page.fill("#firstname", sales_rep["First Name"])
    page.fill("#lastname", sales_rep["Last Name"])
    page.fill("#salesresult", str(sales_rep["Sales"]))
    page.select_option("#salestarget", str(sales_rep["Sales Target"]))
    page.click("text=Submit")


def download_excel_file():
    """Downloads excel file from the given URL"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/SalesData.xlsx", overwrite=True)


def fill_form_with_excel_data():
    """Read data from excel and fill in the sales form"""
    excel = Files()
    excel.open_workbook("SalesData.xlsx")
    worksheet = excel.read_worksheet_as_table("data", header=True)
    excel.close_workbook()

    for row in worksheet:
        fill_and_submit_sales_forms(row)


def collect_results():
    """Take a screenshot of the page"""
    page = browser.page()
    page.screenshot(path="output/sales_summary.png")


def export_as_pdf():
    """Export the data to a pdf file"""
    page = browser.page()
    sales_results_html = page.locator("#sales-results").inner_html()

    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, "output/sales_results.pdf")


def log_out():
    """Presses the 'Log out' button"""
    page = browser.page()  
    page.click("text=Log out")