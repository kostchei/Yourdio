# Voice Samples

This directory holds isolated voice samples for Fish Speech text-to-speech engine fine-tuning or zero-shot reference generation.

## Mako Iwamatsu (Voice Actor)
Located in `samples/Mako/`:

1. **Conan the Barbarian (1982) Introduction**
   - Source: `Mako_Conan_1982_Introduction.mp3` (From YouTube)
   - Isolated Vocals: `Mako_Conan_1982_Introduction_vocals.wav`
   - Description: The classic "Between the time when the oceans drank Atlantis..." intro speech. Excellent theatrical narration voice.

2. **Samurai Jack Introduction**
   - Source: `Mako_Samurai_Jack_Intro.mp3` (From YouTube)
   - Isolated Vocals: `Mako_Samurai_Jack_Intro_vocals.wav`
   - Description: "Long ago in a distant land..." Mako as the voice of Aku, the shape-shifting master of darkness.

### "Mako-omage" Zero-Shot Cloning Strategy
Instead of running a full PyTorch LoRA fine-tuning session (which takes hours and can overfit on minimal data), Fish Speech 1.5 performs exceptionally well with **Zero-Shot Voice Cloning**. 

We have prepared a pristine 20-second reference clip and its exact transcript to instantly clone Mako's voice at runtime:
- **Reference Audio**: `Mako_Samurai_Jack_Reference.wav`
- **Reference Transcript**: "Long ago in a distant land, I, Aku, the shape-shifting master of darkness, unleashed an unspeakable evil! But a foolish Samurai warrior wielding a magic sword stepped forth to oppose me."

By passing both the reference `.wav` file bytes and the exact transcript to the `NarrationClient.speak()` method, the TTS instantly adopts Mako's timbre, pacing, and dramatic intensity for any new text generated!
