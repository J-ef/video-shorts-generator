import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import whisper

# ==============================
# FUNÇÕES
# ==============================

def transcrever(video_path):
    print("\n[1/4] Carregando modelo Whisper...")
    model = whisper.load_model("base")

    print("[2/4] Iniciando transcrição (isso pode demorar)...")
    result = model.transcribe(video_path, verbose=True)

    print("[3/4] Transcrição concluída!")
    return result["segments"]

def gerar_legenda(texto, duracao):
    txt = TextClip(
        texto,
        fontsize=60,
        color='white',
        stroke_color='black',
        stroke_width=2,
        size=(900, None),
        method='caption'
    )
    txt = txt.set_position(('center', 'bottom')).set_duration(duracao)
    return txt

def aplicar_zoom(clip):
    return clip.resize(1.05)


def converter_vertical(clip):
    clip = clip.resize(height=1920)

    if clip.w > 1080:
        clip = clip.crop(x_center=clip.w / 2, width=1080)

    return clip

# ==============================
# MAIN
# ==============================

def gerar_shorts(video_path, max_duration, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video = VideoFileClip(video_path)
    segmentos = transcrever(video_path)

    shorts_gerados = 0
    inicio = 0

    while inicio < video.duration:
        fim = min(inicio + max_duration, video.duration)

        print(f"\nGerando short: {inicio:.2f}s até {fim:.2f}s")

        clip = video.subclip(inicio, fim)

        # Vertical
        clip = converter_vertical(clip)

        # Zoom
        clip = aplicar_zoom(clip)

        clip = clip.set_fps(30)

        clip = clip.set_duration(fim - inicio)

        # Texto
        textos = [
            seg["text"] for seg in segmentos
            if seg["start"] >= inicio and seg["end"] <= fim
        ]

        texto_final = " ".join(textos)[:120]

        if texto_final.strip() != "":
            legenda = gerar_legenda(texto_final, clip.duration)
            clip = CompositeVideoClip([clip, legenda]).set_duration(fim - inicio)

        output_path = os.path.join(output_dir, f"short_{shorts_gerados}.mp4")

        clip.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            preset='medium',
            threads=4
        )

        shorts_gerados += 1
        inicio += max_duration

        print(f"[4/4] Processando trecho {shorts_gerados + 1}")

    print(f"\nTotal de shorts gerados: {shorts_gerados}")

# ==============================
# INTERAÇÃO COM USUÁRIO
# ==============================

if __name__ == "__main__":
    print("=== GERADOR DE SHORTS ===")

    video_path = input("Digite o caminho completo do vídeo: ").strip()

    max_duration = int(input("Digite a duração máxima (em segundos): ").strip())

    output_dir = input("Digite a pasta de saída (ex: C:\\shorts): ").strip()

    gerar_shorts(video_path, max_duration, output_dir)