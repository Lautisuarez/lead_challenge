document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('course-form');
    const errorMsg = document.getElementById('error-msg');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        if(data["start_date"] > data["end_date"]){
            errorMsg.textContent = "The start date cannot be greater than the end date"
            errorMsg.style.display = "block";
            return;
        }

        const body = {
            start_date: data["start_date"],
            end_date: data["end_date"],
            inscription_year: data["inscription_year"],
            lead: {
                name: data["lead_name"],
                last_name: data["lead_last_name"],
                email: data["lead_email"],
                address: data["lead_address"],
                phone: data["lead_phone"]
            },
            subject: {
                name: data["subject_name"],
                career: {
                    name: data["career_name"]
                }
            }
        }

        try {
            const response = await fetch('/api/v1/course/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
            });

            if (!response.ok) {
                errorMsg.textContent = "Oops! An unexpected error occurred... Please try again in a few minutes.";
                errorMsg.style.display = "block";
                throw new Error('Network response was not ok');
            }
            
            errorMsg.style.display = "none";
            const result = await response.json();
            window.location.href = `/${result.id}`
            form.reset();
        } catch (error) {
            errorMsg.textContent = "Oops! An unexpected error occurred... Please try again in a few minutes.";
            errorMsg.style.display = "block";
            console.error('Error:', error);
        }
    });
});