from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uvicorn

app = FastAPI()

# Email config (use Gmail / Outlook / Yahoo SMTP)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "naveenkumar.spacezoneindia@gmail.com"      
SENDER_PASSWORD = "unmd jwaa upji krco"    # ⚠️ Use App Password for Gmail


@app.get("/")
async def health_check():
    return JSONResponse({"status": "working"})

@app.post("/contact")
async def send_contact_form(request: Request):
    try:
        data = await request.json()
        name = data.get("name")
        phone = data.get("phone")
        mail = data.get("mail")
        subject = data.get("subject")
        message = data.get("message")

        # Create email
        msg = MIMEMultipart("alternative")
        msg["From"] = SENDER_EMAIL
        msg["To"] = SENDER_EMAIL   # or forward to another email
        msg["Subject"] = f"📩 New Contact: {subject}"

        # Plain fallback
        text_content = f"""
        New Contact Submission:

        Name: {name}
        Phone: {phone}
        Email: {mail}
        Subject: {subject}
        Message: {message}
        """

        # ✅ Beautiful HTML template (no table)
        html_content = f"""
        <html>
          <body style="margin:0; padding:0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9;">
            <div style="max-width: 600px; margin: 30px auto; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden;">
              
              <div style="background: linear-gradient(135deg, #6a11cb, #2575fc); padding: 20px; color: white;">
                <h2 style="margin:0;">📬 New Contact Form Submission</h2>
              </div>
              
              <div style="padding: 20px; color: #333;">
                <p style="font-size: 15px; margin-bottom: 10px;"><b>Name:</b> {name}</p>
                <p style="font-size: 15px; margin-bottom: 10px;"><b>Phone:</b> {phone}</p>
                <p style="font-size: 15px; margin-bottom: 10px;"><b>Email:</b> {mail}</p>
                <p style="font-size: 15px; margin-bottom: 10px;"><b>Subject:</b> {subject}</p>
                
                <div style="margin-top:20px; padding:15px; background:#f9f9f9; border-left:4px solid #2575fc; border-radius: 6px;">
                  <p style="margin:0; font-size: 14px; color:#444;">{message}</p>
                </div>
              </div>
              
              <div style="background:#f1f1f1; padding:10px; text-align:center; font-size:12px; color:#666;">
                Sent via <b>FastAPI Contact Form</b>
              </div>
            </div>
          </body>
        </html>
        """

        # Attach both plain and HTML
        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        # Send via SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, SENDER_EMAIL, msg.as_string())
        server.quit()

        return JSONResponse({"status": "success", "message": "Styled HTML mail sent successfully!"})

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)})


if __name__ == "__main__":
    uvicorn.run(app)
