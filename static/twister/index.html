<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>3-Wheel Twister Spinner with Speech</title>
    <style>
        /* Basic layout and mobile-friendly setup */
        body {
            margin: 0;
            padding: 0;
            font-family: sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: #f9f9f9;
        }

        h1 {
            margin: 1rem 0 0.5rem;
            font-size: 1.5rem;
            text-align: center;
        }

        .wheels {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
            align-items: center;
            margin-bottom: 1rem;
        }

        /* Common wheel styling */
        .wheel-container {
            position: relative;
            width: 160px;
            height: 160px;
        }

        .wheel {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            transition: transform 3s cubic-bezier(0.33, 1, 0.68, 1);
        }

        .pointer {
            position: absolute;
            top: -4px;
            /* Move up slightly to align with wheel edge */
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-top: 12px solid #333;
            /* Changed from border-bottom to border-top */
            z-index: 1;
            /* Ensure pointer is above the wheel */
        }

        /* Wheel #1: Left / Right */
        /* Conic gradient from 270deg means 0deg is at the top, going clockwise */
        #wheel1 {
            background: conic-gradient(from 270deg,
                    #aaf 0deg 180deg,
                    /* Top half (Left) */
                    #faa 180deg 360deg
                    /* Bottom half (Right) */
                );
        }

        /* Wheel #2: Hand / Foot */
        #wheel2 {
            background: conic-gradient(from 270deg,
                    #aff 0deg 180deg,
                    /* Top half (Hand) */
                    #faf 180deg 360deg
                    /* Bottom half (Foot) */
                );
        }

        /* Wheel #3: 4 colors (Red, Blue, Green, Yellow) */
        #wheel3 {
            background: conic-gradient(from 270deg,
                    red 0deg 90deg,
                    blue 90deg 180deg,
                    green 180deg 270deg,
                    yellow 270deg 360deg);
        }

        /* Text overlays for the first two wheels only */
        .slice-text {
            position: absolute;
            width: 100%;
            text-align: center;
            font-weight: bold;
            color: #333;
            pointer-events: none;
            /* let clicks pass through text */
        }

        /* For a 2-slice wheel: "top" label ~25% down, "bottom" label ~75% down */
        .top-text {
            top: 25%;
            left: 50%;
            transform: translateX(-50%);
        }

        .bottom-text {
            top: 75%;
            left: 50%;
            transform: translateX(-50%);
        }

        /* Controls container */
        .controls {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Spin button */
        .spin-button {
            background-color: #007bff;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 0.5rem;
            font-size: 1rem;
        }

        .spin-button:hover {
            background-color: #005dc1;
        }

        /* Result text */
        #result {
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 1rem;
            text-align: center;
        }

        /* Make wheels smaller on narrower screens for better mobile experience */
        @media (max-width: 600px) {
            .wheel-container {
                width: 120px;
                height: 120px;
            }

            .top-text {
                top: 30%;
            }

            .bottom-text {
                top: 70%;
            }
        }
    </style>
</head>

<body>

    <h1>3-Wheel Twister Spinner</h1>

    <!-- Wheels Container -->
    <div class="wheels">
        <!-- Wheel #1: Left / Right -->
        <div class="wheel-container">
            <div id="wheel1" class="wheel"></div>
            <div class="pointer"></div>
            <!-- Text overlays (top / bottom) -->
            <div class="slice-text top-text">Venstre</div>
            <div class="slice-text bottom-text">Høyre</div>
        </div>

        <!-- Wheel #2: Hand / Foot -->
        <div class="wheel-container">
            <div id="wheel2" class="wheel"></div>
            <div class="pointer"></div>
            <!-- Text overlays -->
            <div class="slice-text top-text">Hånd</div>
            <div class="slice-text bottom-text">Fot</div>
        </div>

        <!-- Wheel #3: Colors -->
        <div class="wheel-container">
            <div id="wheel3" class="wheel"></div>
            <div class="pointer"></div>
        </div>
    </div>

    <!-- Controls: Speak checkbox + Spin button -->
    <div class="controls">
        <label>
            <input type="checkbox" id="speak-toggle" />
            <span role="img" aria-label="loudspeaker">&#128266;</span> Speak result
        </label>

        <button class="spin-button" onclick="spinWheels()">Spin</button>
    </div>

    <!-- Result Display -->
    <div id="result"></div>

    <script>
        // Data sets for each wheel
        const leftRight = ["Venstre", "Høyre"];
        const handFoot = ["Hånd", "Fot"];
        const colors = ["Rød", "Blå", "Grønn", "Gul"];
        const synth = window.speechSynthesis;

        // Track cumulative rotations for each wheel
        let rotation1 = 0;
        let rotation2 = 0;
        let rotation3 = 0;

        function spinWheels() {
            // Each wheel does 5-8 full rotations (5*360 to 8*360),
            // plus a random offset to land in the slice.
            const baseRotations = 360 * (Math.floor(Math.random() * 4) + 5);

            const offset1 = Math.floor(Math.random() * 360);
            const offset2 = Math.floor(Math.random() * 360);
            const offset3 = Math.floor(Math.random() * 360);

            rotation1 += baseRotations + offset1;
            rotation2 += baseRotations + offset2;
            rotation3 += baseRotations + offset3;

            // Apply CSS transforms
            document.getElementById("wheel1").style.transform =
                `rotate(${rotation1}deg)`;
            document.getElementById("wheel2").style.transform =
                `rotate(${rotation2}deg)`;
            document.getElementById("wheel3").style.transform =
                `rotate(${rotation3}deg)`;

            // After 3s, figure out which slice is on top for each wheel
            setTimeout(() => {
                const finalAngle1 = rotation1 % 360;
                const finalAngle2 = rotation2 % 360;
                const finalAngle3 = rotation3 % 360;

                // 2-slice wheels: 0..180 => index 0, 180..360 => index 1
                const index1 = Math.floor(finalAngle1 / 180);
                const index2 = Math.floor(finalAngle2 / 180);

                // 4-slice wheel: each slice = 90 degrees
                const index3 = Math.floor(finalAngle3 / 90);

                const side = leftRight[index1];  // "Left" or "Right"
                const limb = handFoot[index2];   // "Hand" or "Foot"
                const color = colors[index3];    // "Red", "Blue", "Green", "Yellow"

                const resultText = `Sett ${side} ${limb} på ${color}`;
                // Display the final result
                document.getElementById("result").textContent = resultText;

                // Check if the "Speak result" checkbox is checked
                const speakToggle = document.getElementById("speak-toggle");
                if (speakToggle.checked) {
                    speakResult(resultText);
                }
            }, 3000);
        }

        function speakResult(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            // You can configure more TTS options here, e.g. voice, pitch, rate
            // set voice to Nora (nb-NO) if available, otherwise use default
            utterance.voice = synth.getVoices().find(v => v.lang === "nb-NO") ||
                synth.getVoices().find(v => v.lang === "en-US");
            synth.speak(utterance);
        }
    </script>
</body>

</html>