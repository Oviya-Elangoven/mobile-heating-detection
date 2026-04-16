import streamlit as st
from win10toast import ToastNotifier
import threading

toaster = ToastNotifier()

def send_toast(risk):

    toaster.show_toast(
        "Thermal Risk Alert",
        f"Device overheating detected!\nRisk = {risk:.1f}",
        duration=5,
        threaded=True
    )

def check_alert(risk):

    if "alert_sent" not in st.session_state:
        st.session_state.alert_sent = False

    if risk > 70 and not st.session_state.alert_sent:

        st.error("🚨 CRITICAL HEATING ALERT!")

        threading.Thread(
            target=send_toast,
            args=(risk,),
            daemon=True
        ).start()

        st.session_state.alert_sent = True

    elif risk <= 70:
        st.session_state.alert_sent = False
