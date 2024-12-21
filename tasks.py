from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Indistries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(slowmo = 100)
    open_robot_order_website()
    download_orders_file()
    fill_form_with_csv_data()
    archive_receipts()

def open_robot_order_website():
    """Navigats to the Robot Order website and accept the pop up"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    close_annoying_modal()

def close_annoying_modal():
    page = browser.page()
    page.click("text=OK")

def order_another_robot():
    """Clicks on 'Order Another Robot' button"""
    page = browser.page()
    page.click("#order-another")

def download_orders_file():
    """Downloads the orders CVS file"""
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)

def fill_and_submit_order_form(robot_order):
    """Fills the order form and click the 'Order' button"""
    page = browser.page()

    page.select_option("#head", str(robot_order["Head"]))
    page.click(f"#id-body-{robot_order["Body"]}")
    page.fill("input[placeholder='Enter the part number for the legs']", str(robot_order["Legs"]))
    page.fill("#address", str(robot_order["Address"]))
    page.click("text=Preview")

    while True:
        page.click("#order")
        order_another = page.query_selector("#order-another")
        if order_another:
            store_receipt_as_pdf(int(robot_order["Order number"]))
            screenshot_path = screenshot_robot(int(robot_order["Order number"]))
            embed_screenshot_to_receipt(screenshot_path, robot_order["Order number"])
            order_another_robot()
            close_annoying_modal()
            break

def fill_form_with_csv_data():
    """Read data from csv and fill in the sales form"""
    csv_file = Tables()
    order_robot_data = csv_file.read_table_from_csv("orders.csv")

    for row in order_robot_data:
        fill_and_submit_order_form(row)

def store_receipt_as_pdf(order_number):
    """Store the order recipt as a PDF file"""
    page = browser.page()
    order_results_html = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf_path = f"output/receipts/{order_number}.pdf"
    pdf.html_to_pdf(order_results_html, pdf_path)
    return pdf_path

def screenshot_robot(order_number):
    """Takes a screenshot of the receipt"""
    page = browser.page()
    screenshot_path = f"output/screenshots/{order_number}.png"
    page.locator("#robot-preview-image").screenshot(path=screenshot_path)
    return screenshot_path

def embed_screenshot_to_receipt(screenshot_path, order_number):
    """Embeds the robot screenshot to the receipt PDF file"""
    pdf = PDF()
    list_of_files = [screenshot_path]
    pdf.add_files_to_pdf(files=list_of_files, target_document=f"output/receipts/{order_number}.pdf", append=True)

def archive_receipts():
    """Archives the file of receipt PDF files"""
    data_archive = Archive()
    data_archive.archive_folder_with_zip("output/receipts/", "Merged_Robot_Orders.zip")


