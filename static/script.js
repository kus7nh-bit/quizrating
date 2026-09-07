let answers = {};


// ========================================
// QUESTIONS
// ========================================

const questions = [
    "How satisfied are you with the current process?",
    "How good is the communication within the team?",
    "How satisfied are you with the work environment?",
    "How would you rate team collaboration?",
    "How satisfied are you with management support?"
];


// ========================================
// RATING BUTTONS
// ========================================

document.querySelectorAll(".question").forEach((question, index) => {

    const buttons =
        question.querySelectorAll(".rating button");

    buttons.forEach(button => {

        button.addEventListener("click", function () {

            const rating =
                Number(this.dataset.rating);

            answers[index] = rating;

            buttons.forEach(btn => {
                btn.classList.remove("selected");
            });

            this.classList.add("selected");

        });

    });

});


// ========================================
// SUBMIT SURVEY
// ========================================

async function submitSurvey() {

    const personName =
        document.getElementById("personName").value.trim();

    if (!personName) {
        alert("Please enter your name.");
        return;
    }

    if (Object.keys(answers).length < questions.length) {
        alert("Please answer all questions.");
        return;
    }

    // Convert answers into the format Flask expects
    const formattedAnswers = questions.map((question, index) => {

        return {
            question: question,
            rating: Number(answers[index])
        };

    });

    try {

        const response = await fetch("/submit", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                personName: personName,

                answers: formattedAnswers

            })

        });


        const data = await response.json();


        if (data.success) {

            alert("Submitted successfully!");

            // Refresh the survey
            window.location.reload();

        } else {

            alert(data.message || "Something went wrong.");

        }

    } catch (error) {

        console.error("Submit error:", error);

        alert("Something went wrong while submitting.");

    }

}