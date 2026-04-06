from music21 import converter, stream, tempo, instrument, note, chord
import copy

arquivo_xml = r"F:\Projetos de Musica\Musica para Games\xml\entertainer.mxl"
arquivo_midi = r"F:\Projetos de Musica\Musica para Games\midi\entertainer3.mid"

score_original = converter.parse(arquivo_xml)

# Define BPM fixo
bpm = 90
score_original.insert(0, tempo.MetronomeMark(number=bpm))

right_hand = stream.Part()
left_hand = stream.Part()

right_hand.insert(0, instrument.Piano())
left_hand.insert(0, instrument.Piano())

for elemento in score_original.recurse().notes:

    # Se for nota simples
    if isinstance(elemento, note.Note):
        nova = copy.deepcopy(elemento)
        nova.volume.velocity = 85

        if elemento.pitch.midi >= 60:
            right_hand.append(nova)
        else:
            left_hand.append(nova)

    # Se for acorde
    elif isinstance(elemento, chord.Chord):
        notas_direita = []
        notas_esquerda = []

        for p in elemento.pitches:
            if p.midi >= 60:
                notas_direita.append(p)
            else:
                notas_esquerda.append(p)

        if notas_direita:
            acorde_dir = chord.Chord(notas_direita)
            acorde_dir.duration = elemento.duration
            acorde_dir.volume.velocity = 85
            right_hand.append(acorde_dir)

        if notas_esquerda:
            acorde_esq = chord.Chord(notas_esquerda)
            acorde_esq.duration = elemento.duration
            acorde_esq.volume.velocity = 85
            left_hand.append(acorde_esq)

novo_score = stream.Score()
novo_score.insert(0, right_hand)
novo_score.insert(0, left_hand)

novo_score.write("midi", arquivo_midi)

print("MIDI otimizado para LMMS gerado com sucesso!")