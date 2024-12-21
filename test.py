# from robocorp.tasks import task
# from robocorp import browser

# from RPA.HTTP import HTTP
# from RPA.Tables import Tables

# @task
# def order_robots_from_RobotSpareBin():
#     """
#     Orders robots from RobotSpareBin Indistries Inc.
#     Saves the order HTML receipt as a PDF file.
#     Saves the screenshot of the ordered robot.
#     Embeds the screenshot of the robot to the PDF receipt.
#     Creates ZIP archive of the receipts and the images.
#     """
#     browser.configure(slowmo = 500)
#     open_robot_order_website()
#     download_orders_file()
#     fill_and_submit_order_form()

# def open_robot_order_website():
#     """Navigats to the Robot Order website and accept the pop up"""
#     browser.goto("https://robotsparebinindustries.com/#/robot-order")
#     close_annoying_modal()

# def close_annoying_modal():
#     page = browser.page()
#     page.click("text=OK")

# def download_orders_file():
#     """Downloads the orders CVS file"""
#     http = HTTP()
#     http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)

# def fill_and_submit_order_form():
#     """Fills the order form and click the 'Order' button"""
#     page = browser.page()

#     page.select_option("#head", "Roll-a-thor head")
#     page.click("#id-body-2")
#     page.fill("input[placeholder='Enter the part number for the legs']", "3")
#     page.fill("#address", "Address 123")
#     page.click("text=Preview")
#     page.click("text=Order")

# ____________________ Test 2 ________________________________

from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Indistries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(slowmo = 500)
    open_robot_order_website()
    download_orders_file()
    fill_form_with_csv_data()

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
    
    page.click("#order")
    order_another_robot()
    close_annoying_modal()

def fill_form_with_csv_data():
    """Read data from csv and fill in the sales form"""
    csv_file = Tables()
    order_robot_data = csv_file.read_table_from_csv("orders.csv")

    for row in order_robot_data:
        fill_and_submit_order_form(row)

