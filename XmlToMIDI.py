from music21 import converter
import os

arquivo_xml = r"F:\Projetos de Musica\Musica para Games\xml\entertainer.mxl"
arquivo_midi = r"F:\Projetos de Musica\Musica para Games\midi\entertainer.mid"

if not os.path.exists(arquivo_xml):
    print("Arquivo XML não encontrado!")
else:
    score = converter.parse(arquivo_xml)
    score.write("midi", arquivo_midi)
    print("MIDI gerado com sucesso!")