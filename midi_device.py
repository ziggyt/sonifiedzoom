import mido


class MidiDevice:
    MIDI_MAX = 80
    MIDI_MIN = 10

    virtual_midi_out = mido.open_output('Sonified Zoom', virtual=True)

    def send_midi_note(self, note: int, state: bool = True):
        midi_state = 'note_on' if state else 'note_off'

        msg = mido.Message(midi_state, note=note)

        self.virtual_midi_out.send(msg)

    def send_midi_note_to_channel(self, note: int, channel: int, state: bool = True):
        if 0 < note > 127:
            raise Exception(f"Unacceptable note input: {note}")

        if 0 < channel > 15:
            raise Exception(f"Unacceptable channel input: {channel}")

        midi_state = 'note_on' if state else 'note_off'

        msg = mido.Message(midi_state, note=note, channel=channel)

        self.virtual_midi_out.send(msg)

    def turn_off_all_notes(self):
        self.virtual_midi_out.reset()
        #
        # for i in range(127):
        #     self.send_midi_note(i, False)

    def send_cc_message(self, value: int, channel: int):
        if 0 < value > 127:
            raise Exception(f"Unacceptable value input: {value}")

        if 0 < channel > 15:
            raise Exception(f"Unacceptable channel input: {channel}")

        msg = mido.Message(type="control_change", control=channel, value=value)

        print(f'sent cc message with value {value} on channel {channel}')

        self.virtual_midi_out.send(msg)
