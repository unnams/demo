from mcp.server.fastmcp import FastMCP
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
import sys
load_dotenv()

mcp = FastMCP("Expense Approval Service")

# Approver Emails
APPROVERS = {
    "Manager": "pranathip029@gmail.com",
    "Director": "mahidhark2003@gmail.com",
    "CFO":     "praneethunnam@gmail.com"
}


# Email Sending Function
def send_email(to: str, subject: str, body: str):
    try:
        msg = EmailMessage()
        msg["From"] = os.getenv("SENDER_EMAIL")
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(
                os.getenv("SENDER_EMAIL"),
                os.getenv("EMAIL_PASSWORD")
            )
            server.send_message(msg)

        return "Email sent successfully"

    except Exception as e:
        print("Email error:", e, file=sys.stderr)
        return f"Email failed: {e}"


# MCP Tool
@mcp.tool()
def process_expense(employee: str, amount: float, purpose: str):
    try:
        print("Processing expense...", file=sys.stderr)

        # Determine approver
        if amount <= 10000:
            approver_role = "Manager"
        elif amount <= 50000:
            approver_role = "Director"
        else:
            approver_role = "CFO"

        approver_email = APPROVERS.get(approver_role)

        if not approver_email:
            return "Approver role not configured."

        subject = f"Expense Approval Required - ₹{amount}"

        body = f"""
Dear {approver_role},

Please review the following expense request:

Employee: {employee}
Amount: ₹{amount}
Purpose: {purpose}

Kindly review and approve.

Regards,
Expense Approval System
"""

        # Send Email
        email_status = send_email(approver_email, subject, body)

        return f"Expense sent to {approver_role} ({approver_email}). Status: {email_status}"

    except Exception as e:
        print("Processing error:", e, file=sys.stderr)
        return f"Processing failed: {e}"


if __name__ == "__main__":
    print("Starting MCP Expense Approval Server...", file=sys.stderr)
    mcp.run(transport="stdio")
    



