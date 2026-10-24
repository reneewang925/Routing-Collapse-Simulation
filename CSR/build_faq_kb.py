import json

# 捏造几段又臭又长的客服政策文档（模拟真实世界里的冗余信息）
faq_docs = [
    {
        "doc_id": "faq_doc_1",
        "text": "Refund Policy: We want you to be completely satisfied with your purchase. If you are not satisfied, you may request a refund within 30 days of the original purchase date. To request a refund, please go to the 'My Orders' section of our website, select the item you wish to return, and click 'Request Refund'. Please note that items must be in their original packaging and unused. Once we receive your return, it may take 5-7 business days for the refund to be processed and reflected in your original payment method. Shipping costs are non-refundable. If the item was damaged upon arrival, please contact customer support immediately with photos of the damage."
    },
    {
        "doc_id": "faq_doc_2",
        "text": "Shipping and Delivery: We offer standard and expedited shipping options. Standard shipping usually takes 5 to 7 business days, while expedited shipping takes 2 to 3 business days. Please note that order processing takes 1-2 business days before shipment. Once your order has shipped, you will receive a tracking number via email. You can use this tracking number to monitor the status of your package on our carrier's website. If your package has not arrived within the estimated delivery time, please check with your local post office or contact our support team."
    },
    {
        "doc_id": "faq_doc_3",
        "text": "Account and Password: If you have forgotten your password, click on the 'Forgot Password' link on the login page. Enter the email address associated with your account, and we will send you an email with a link to reset your password. If you do not receive the email within 15 minutes, please check your spam folder or ensure you entered the correct email address. For security reasons, we recommend using a strong, unique password that includes a combination of letters, numbers, and special characters."
    },
    {
        "doc_id": "faq_doc_4",
        "text": "Subscription Cancellation: You can cancel your subscription at any time from your account dashboard. Go to 'Account Settings' -> 'Subscriptions' and click 'Cancel Subscription'. Your subscription will remain active until the end of your current billing cycle, and you will not be charged for the next cycle. We do not offer prorated refunds for partial months. If you cancel within 14 days of your initial purchase, you may be eligible for a full refund under our money-back guarantee."
    },
    {
        "doc_id": "faq_doc_5",
        "text": "Contact Information: Our customer support team is available Monday through Friday, 9:00 AM to 5:00 PM EST. You can reach us by email at support@example.com or by calling 1-800-123-4567. For faster service, please have your order number ready when you contact us. We strive to respond to all emails within 24 hours."
    }
]

with open("faq_kb.json", "w", encoding="utf-8") as f:
    json.dump(faq_docs, f, indent=2, ensure_ascii=False)

print("✅ 成功！已生成低风险知识库：faq_kb.json，共", len(faq_docs), "个文档块")