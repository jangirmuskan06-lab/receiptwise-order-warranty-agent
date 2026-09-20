import hashlib
from pathlib import Path

import streamlit as st

from agent import (
    create_proactive_summary,
    answer_followup_with_evidence,
)
from ingestion import build_receipt_retriever
from tools import lookup_order_status


st.set_page_config(
    page_title="ReceiptWise",
    page_icon="🛍️",
    layout="wide",
)
if st.button(
    f"Check return requirements for {item['name']}",
    key=f"return_requirements_{item['name']}",
):
    st.session_state["pending_question"] = (
        f"What are the return requirements for {item['name']}?"
    )

    st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f8fbff 0%, #ffffff 45%);
    }

    .main-title {
        font-size: 2.7rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0;
    }

    .sub-title {
        color: #475569;
        font-size: 1.08rem;
        margin-bottom: 1rem;
    }

    .trust-banner {
        background: #e0f2fe;
        border: 1px solid #7dd3fc;
        border-radius: 14px;
        color: #0c4a6e;
        padding: 12px 16px;
        margin: 12px 0 24px 0;
        font-weight: 600;
    }

    .item-card {
        background: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }

    .footer-note {
        color: #64748b;
        text-align: center;
        font-size: 0.85rem;
        padding: 30px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<p class="main-title">🛍️ ReceiptWise</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Instant return, warranty and live-order assistant</p>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload your receipt or order confirmation",
    type=["txt"],
    help="Use the sample receipt format created earlier.",
)

if uploaded_file is None:
    st.info("Upload a receipt to immediately see return and warranty deadlines.")

    st.markdown("### How it works")

    step_one, step_two, step_three = st.columns(3)

    with step_one:
        st.write("**1. Upload**")
        st.caption("Add your order confirmation or receipt.")

    with step_two:
        st.write("**2. Review Return Radar**")
        st.caption("See deadlines and expiring-soon alerts before asking.")

    with step_three:
        st.write("**3. Ask or track**")
        st.caption("Ask a policy question or check live order status.")

    with st.expander("View supported receipt format"):
        st.code(
            "Order ID: ORD-1001\n"
            "Purchase Date: 2026-08-26\n\n"
            "1. Alpine Winter Jacket | Category: Clothing | Price: $120.00"
        )

    st.caption(
        "ReceiptWise only uses the uploaded receipt and store policy "
        "to answer questions."
    )

    st.stop()

receipt_text = uploaded_file.getvalue().decode("utf-8")
receipt_hash = hashlib.md5(receipt_text.encode("utf-8")).hexdigest()

if st.session_state.get("receipt_hash") != receipt_hash:
    try:
        with st.spinner("Reading receipt, checking policy windows, and preparing search..."):
            policy_text = Path("data/policy.txt").read_text(encoding="utf-8")

            retriever, items, order_id = build_receipt_retriever(
                receipt_text,
                policy_text,
            )

            proactive_summary = create_proactive_summary(items)

            st.session_state["receipt_hash"] = receipt_hash
            st.session_state["retriever"] = retriever
            st.session_state["items"] = items
            st.session_state["order_id"] = order_id
            st.session_state["proactive_summary"] = proactive_summary
            st.session_state["messages"] = []

    except Exception as error:
        st.info(
    "Check that your receipt includes an Order ID, Purchase Date, "
    "and item lines with name, category, and price."
)
        st.stop()

st.success(
    f"Receipt analyzed for order {st.session_state['order_id']}. "
    "Your deadlines are ready."
)

# Return Radar: proactive deadline dashboard
all_records = st.session_state["proactive_summary"]

urgent_records = [
    record for record in all_records
    if record["return_window"]["expiring_soon"]
]

expired_records = [
    record for record in all_records
    if record["return_window"]["expired"]
]

safe_records = [
    record for record in all_records
    if (
        not record["return_window"]["expired"]
        and not record["return_window"]["expiring_soon"]
    )
]

st.header("Return Radar")

metric_1, metric_2, metric_3 = st.columns(3)

metric_1.metric(
    "Needs attention",
    len(urgent_records),
    "Return deadline close" if urgent_records else "No urgent deadlines",
)

metric_2.metric(
    "Expired returns",
    len(expired_records),
)

metric_3.metric(
    "Return-safe items",
    len(safe_records),
)

if urgent_records:
    st.warning(
        f"⚠️ Act soon: {len(urgent_records)} item has a return window "
        "that expires in fewer than 7 days."
    )
elif expired_records:
    st.info(
        "Some return windows have expired, but active warranty coverage "
        "is shown below."
    )
else:
    st.success("All active return windows are currently safe.")

view_filter = st.radio(
    "Show items",
    ["All items", "Needs attention", "Expired returns"],
    horizontal=True,
)

if view_filter == "Needs attention":
    radar_items = urgent_records
elif view_filter == "Expired returns":
    radar_items = expired_records
else:
    radar_items = all_records

for record in radar_items:
    item = record["item"]
    return_window = record["return_window"]

    with st.container(border=True):
        top_left, top_right = st.columns([3, 2])

        with top_left:
            st.subheader(item["name"])
            st.caption(f"{item['category']} · {item['price']}")

        with top_right:
            if return_window["expired"]:
                st.error("Return window expired")
            elif return_window["expiring_soon"]:
                st.warning(
                    f"⚠️ {return_window['days_remaining']} days left"
                )
            else:
                st.success(
                    f"✓ {return_window['days_remaining']} days left"
                )

        st.write(f"Return deadline: **{return_window['deadline']}**")

        if not return_window["expired"]:
            progress_value = min(
                return_window["days_remaining"]
                / return_window["policy_days"],
                1.0,
            )
            st.progress(progress_value)
st.header("Your purchase summary")

for record in st.session_state["proactive_summary"]:
    item = record["item"]
    return_window = record["return_window"]
    warranty_window = record["warranty_window"]

    st.markdown('<div class="item-card">', unsafe_allow_html=True)

    left, middle, right = st.columns([2, 2, 2])

    with left:
        st.subheader(item["name"])
        st.write(f"Category: {item['category']}")
        st.write(f"Price: {item['price']}")

    with middle:
        st.write("**Return window**")

        if return_window["expired"]:
            st.error(
                f"Expired on {return_window['deadline']}"
            )
        elif return_window["expiring_soon"]:
            st.warning(
                f"⚠️ Expiring soon: {return_window['days_remaining']} days left"
            )
            st.write(f"Return deadline: {return_window['deadline']}")
        else:
            st.success(
                f"{return_window['days_remaining']} days left"
            )
            st.write(f"Return deadline: {return_window['deadline']}")

    with right:
        st.write("**Warranty window**")

        if warranty_window["expired"]:
            st.error(f"Expired on {warranty_window['deadline']}")
        else:
            st.info(
                f"{warranty_window['days_remaining']} days remaining"
            )
            st.write(f"Warranty ends: {warranty_window['deadline']}")

    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.header("Track an order")

status_order_id = st.text_input(
    "Enter an order ID",
    placeholder="Example: ORD-1001",
)

if st.button("Check live order status"):
    if not status_order_id.strip():
        st.warning("Enter an order ID first.")
    else:
        result = lookup_order_status.invoke({
            "order_id": status_order_id
        })

        if result["found"]:
            st.success(f"Order {result['order_id']}: {result['status']}")
            st.write(f"Tracking number: {result['tracking_number']}")
            st.write(f"Estimated delivery: {result['estimated_delivery']}")
        else:
            st.error(result["message"])

st.divider()

st.header("Ask about this receipt")

for message in st.session_state["messages"]:
st.session_state["pending_question"] = None
    with st.chat_message(message["role"]):
        st.write(message["content"])

typed_question = st.chat_input(
    "Example: When can I return the jacket?"
)

question = st.session_state.get("pending_question") or typed_question
st.session_state["pending_question"] = None
)

if question:
    st.session_state["messages"].append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Checking your receipt and store policy..."):
            result = answer_followup_with_evidence(
    question,
    st.session_state["retriever"],
)

answer = result["answer"]
st.write(answer)
with st.expander("How ReceiptWise checked this", expanded=False):
    if result["actions"]:
        for step_number, action in enumerate(result["actions"], start=1):
            st.write(f"{step_number}. {action}")
    else:
        st.write("No additional tools were needed for this answer.")

with st.expander("View sources used for this answer"):
    for evidence in result["evidence"]:
        st.caption(f"Source: {evidence['source']}")
        st.write(evidence["content"])

    st.session_state["messages"].append({
        "role": "assistant",
        "content": answer,
    })
st.markdown(
    '<p class="footer-note">'
    'ReceiptWise · Proactive return and warranty protection'
    '</p>',
    unsafe_allow_html=True,
)