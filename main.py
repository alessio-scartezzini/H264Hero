#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

# Estensioni video supportate
VIDEO_EXTENSIONS = [".avi", ".mkv", ".mov", ".wmv", ".flv", ".ts", ".webm", ".mp4"]

def detect_acceleration():
    """
    Rileva automaticamente quale accelerazione hardware è disponibile:
    - Intel QuickSync (h264_qsv)
    - NVIDIA NVENC (h264_nvenc)
    - AMD AMF (h264_amf)
    - Fallback CPU (libx264)
    """
    result = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True)
    encoders = result.stdout.lower()

    if "h264_qsv" in encoders:
        print("[INFO] Usando GPU Intel QuickSync")
        return "h264_qsv", "-hwaccel qsv"
    elif "h264_nvenc" in encoders:
        print("[INFO] Usando GPU NVIDIA NVENC")
        return "h264_nvenc", None
    elif "h264_amf" in encoders:
        print("[INFO] Usando GPU AMD AMF")
        return "h264_amf", None
    else:
        print("[INFO] Nessuna GPU disponibile, usando CPU (libx264)")
        return "libx264", None

def convert_to_mp4(input_file, video_codec, hwaccel_flag):
    """
    Converte un file video in MP4 H.264 + AAC.
    Crea un nuovo file con suffisso '_converted'.
    Salta file già in H.264 + AAC.
    """
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_converted.mp4"

    # Salta se file già in H.264
    if ext.lower() == ".mp4":
        cmd_probe = ["ffprobe", "-v", "error", "-select_streams", "v:0",
                     "-show_entries", "stream=codec_name", "-of",
                     "default=nokey=1:noprint_wrappers=1", input_file]
        result = subprocess.run(cmd_probe, capture_output=True, text=True)
        if "h264" in result.stdout:
            print(f"[SKIP] File già in H.264: {os.path.basename(input_file)}")
            return

    cmd = ["ffmpeg", "-y"]
    if hwaccel_flag:
        cmd.extend([hwaccel_flag])
    cmd.extend([
        "-i", input_file,
        "-c:v", video_codec,
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output_file
    ])

    try:
        subprocess.run(cmd, check=True)
        print(f"[OK] Convertito: {os.path.basename(input_file)} -> {os.path.basename(output_file)}")
    except subprocess.CalledProcessError:
        print(f"[ERRORE] Conversione fallita per {os.path.basename(input_file)}")

def main():
    print("Seleziona l'opzione:")
    print("1) Convertire un singolo file")
    print("2) Convertire più file selezionati")
    print("3) Convertire tutti i video in una cartella")
    choice = input("Scelta (1/2/3): ").strip()

    video_codec, hwaccel_flag = detect_acceleration()

    if choice == "1":
        file_path = input("Inserisci il percorso del video: ").strip()
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in VIDEO_EXTENSIONS:
            convert_to_mp4(file_path, video_codec, hwaccel_flag)
        else:
            print("❌ File non valido o estensione non supportata")

    elif choice == "2":
        files = input("Inserisci i percorsi dei video separati da virgola: ").strip().split(",")
        for file_path in files:
            file_path = file_path.strip()
            if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in VIDEO_EXTENSIONS:
                convert_to_mp4(file_path, video_codec, hwaccel_flag)
            else:
                print(f"❌ File non valido o estensione non supportata: {file_path}")

    elif choice == "3":
        folder = input("Inserisci il percorso della cartella con i video: ").strip()
        if not os.path.isdir(folder):
            print("❌ Cartella non valida")
            return
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS:
                convert_to_mp4(file_path, video_codec, hwaccel_flag)
    else:
        print("❌ Scelta non valida")

if __name__ == "__main__":
    main()
