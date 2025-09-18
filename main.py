#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

# Estensioni video supportate
VIDEO_EXTENSIONS = [".avi", ".mkv", ".mov", ".wmv", ".flv", ".ts", ".webm", ".mp4"]

def detect_acceleration():
    """
    Rileva quale accelerazione hardware è disponibile per la codifica:
    - Intel QuickSync (h264_qsv)
    - NVIDIA NVENC (h264_nvenc)
    - AMD AMF (h264_amf)
    - Fallback CPU (libx264)
    """
    result = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True)
    encoders = result.stdout.lower()

    if "h264_qsv" in encoders:
        print("[INFO] Usando GPU Intel QuickSync")
        return "h264_qsv"
    elif "h264_nvenc" in encoders:
        print("[INFO] Usando GPU NVIDIA NVENC")
        return "h264_nvenc"
    elif "h264_amf" in encoders:
        print("[INFO] Usando GPU AMD AMF")
        return "h264_amf"
    else:
        print("[INFO] Nessuna GPU disponibile, usando CPU (libx264)")
        return "libx264"

def is_valid_video(file_path):
    """Verifica se un file video è leggibile da ffprobe"""
    try:
        subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            check=True, capture_output=True, text=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def convert_to_mp4(input_file, video_codec):
    """
    Converte un file video in MP4 H.264 + AAC.
    Se la conversione va a buon fine:
      - sposta il file convertito in 'convertiti'
      - elimina il file originale
    """
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_converted.mp4"
    output_folder = os.path.join(os.path.dirname(input_file), "convertiti")
    os.makedirs(output_folder, exist_ok=True)

    # Controllo se il file è già convertito
    if "_converted.mp4" in input_file:
        if is_valid_video(input_file):
            # Se il file convertito è valido, elimina l'originale corrispondente
            original_file = input_file.replace("_converted.mp4", ext)
            if os.path.exists(original_file):
                os.remove(original_file)
                print(f"[OK] File convertito valido, eliminato originale: {original_file}")
        else:
            print(f"[ERRORE] File convertito corrotto o non leggibile: {input_file}")
        return

    # Salta se file già in H.264
    if ext.lower() == ".mp4":
        cmd_probe = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=codec_name", "-of",
            "default=nokey=1:noprint_wrappers=1", input_file
        ]
        result = subprocess.run(cmd_probe, capture_output=True, text=True)
        if "h264" in result.stdout:
            # Genera percorso convertito previsto
            converted_path = os.path.join(output_folder, os.path.basename(f"{base}_converted.mp4"))
            if os.path.exists(converted_path) and is_valid_video(converted_path):
                os.remove(input_file)
                print(f"[SKIP] File già in H.264 e convertito valido, eliminato originale: {input_file}")
            else:
                print(f"[SKIP] File già in H.264: {input_file}")
            return

    # Comando di conversione
    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-c:v", video_codec,
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output_file
    ]

    try:
        subprocess.run(cmd, check=True)
        # Sposta il file convertito nella cartella convertiti
        final_path = os.path.join(output_folder, os.path.basename(output_file))
        os.replace(output_file, final_path)
        # Elimina il file originale
        os.remove(input_file)
        print(f"[OK] Convertito: {os.path.basename(input_file)} -> {final_path} (originale eliminato)")
    except subprocess.CalledProcessError:
        print(f"[ERRORE] Conversione fallita per {os.path.basename(input_file)}")

def main():
    print("Seleziona l'opzione:")
    print("1) Convertire un singolo file")
    print("2) Convertire più file selezionati")
    print("3) Convertire tutti i video in una cartella")
    choice = input("Scelta (1/2/3): ").strip()

    video_codec = detect_acceleration()

    if choice == "1":
        file_path = input("Inserisci il percorso del video: ").strip()
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in VIDEO_EXTENSIONS:
            convert_to_mp4(file_path, video_codec)
        else:
            print("❌ File non valido o estensione non supportata")

    elif choice == "2":
        files = input("Inserisci i percorsi dei video separati da virgola: ").strip().split(",")
        for file_path in files:
            file_path = file_path.strip()
            if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in VIDEO_EXTENSIONS:
                convert_to_mp4(file_path, video_codec)
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
                convert_to_mp4(file_path, video_codec)
    else:
        print("❌ Scelta non valida")

if __name__ == "__main__":
    main()
