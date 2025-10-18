from ultralytics import YOLO
import streamlit as st

def load_model() -> YOLO:
    try:
        return YOLO('./best.pt')
    except FileNotFoundError:
        return None
