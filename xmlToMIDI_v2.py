from music21 import converter, tempo, midi


arquivo_xml = r"F:\Projetos de Musica\Musica para Games\xml\entertainer.mxl"
arquivo_midi = r"F:\Projetos de Musica\Musica para Games\midi\entertainer2.mid"

score = converter.parse(arquivo_xml)

# Define BPM fixo
bpm = 90
score.insert(0, tempo.MetronomeMark(number=bpm))

# Normaliza velocity
for n in score.recurse().notes:
    n.volume.velocity = 80  # valor médio fixo

score.write("midi", arquivo_midi)

print("MIDI gerado com BPM fixo e velocity normalizada!")