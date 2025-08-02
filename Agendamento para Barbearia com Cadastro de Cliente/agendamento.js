// Agendamento functionality for Barbearia Clássica

let currentStep = 1;
let formData = {};

// Step navigation functions
function nextStep(step) {
    if (step === 2 && !validateForm()) {
        return;
    }
    
    if (step === 3 && !validateDateTime()) {
        return;
    }
    
    // Save current step data
    saveStepData();
    
    // Hide current step
    document.querySelector(`#step${currentStep}`).classList.remove('active');
    document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove('active');
    
    // Show next step
    currentStep = step;
    document.querySelector(`#step${currentStep}`).classList.add('active');
    document.querySelector(`.step[data-step="${currentStep}"]`).classList.add('active');
    
    // If moving to confirmation step, populate data
    if (step === 3) {
        populateConfirmation();
    }
}

function prevStep(step) {
    // Hide current step
    document.querySelector(`#step${currentStep}`).classList.remove('active');
    document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove('active');
    
    // Show previous step
    currentStep = step;
    document.querySelector(`#step${currentStep}`).classList.add('active');
    document.querySelector(`.step[data-step="${currentStep}"]`).classList.add('active');
}

function saveStepData() {
    if (currentStep === 1) {
        formData.nome = document.getElementById('nome').value;
        formData.email = document.getElementById('email').value;
        formData.telefone = document.getElementById('telefone').value;
    } else if (currentStep === 2) {
        const dateTime = window.calendar.getSelectedDateTime();
        if (dateTime) {
            formData.data = dateTime.date;
            formData.horario = dateTime.time;
            formData.dataFormatada = dateTime.dateString;
        }
    }
}

function validateDateTime() {
    const dateTime = window.calendar.getSelectedDateTime();
    if (!dateTime) {
        alert('Por favor, selecione uma data e horário.');
        return false;
    }
    return true;
}

function populateConfirmation() {
    document.getElementById('confirm-nome').textContent = formData.nome;
    document.getElementById('confirm-email').textContent = formData.email;
    document.getElementById('confirm-telefone').textContent = formData.telefone;
    document.getElementById('confirm-data').textContent = formData.dataFormatada;
    document.getElementById('confirm-horario').textContent = formData.horario;
}

// Form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('agendamentoForm');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Save final step data
            saveStepData();
            
            // Show loading modal
            showModal('loadingModal');
            
            try {
                // Prepare data for submission
                const submitData = {
                    nome: formData.nome,
                    email: formData.email,
                    telefone: formData.telefone,
                    data: formData.data.toISOString().split('T')[0], // YYYY-MM-DD format
                    horario: formData.horario
                };
                
                // Submit to backend
                const response = await fetch('/api/agendamento', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(submitData)
                });
                
                const result = await response.json();
                
                // Hide loading modal
                closeModal('loadingModal');
                
                if (response.ok) {
                    // Show success modal
                    showModal('successModal');
                    
                    // Reset form after success
                    setTimeout(() => {
                        resetForm();
                    }, 3000);
                } else {
                    throw new Error(result.message || 'Erro ao processar agendamento');
                }
                
            } catch (error) {
                // Hide loading modal
                closeModal('loadingModal');
                
                // Show error message
                alert('Erro ao processar agendamento: ' + error.message);
                console.error('Error:', error);
            }
        });
    }
});

function resetForm() {
    // Reset form data
    formData = {};
    currentStep = 1;
    
    // Reset form fields
    document.getElementById('agendamentoForm').reset();
    
    // Reset steps
    document.querySelectorAll('.form-step').forEach(step => {
        step.classList.remove('active');
    });
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active');
    });
    
    // Show first step
    document.getElementById('step1').classList.add('active');
    document.querySelector('.step[data-step="1"]').classList.add('active');
    
    // Reset calendar
    if (window.calendar) {
        window.calendar.selectedDate = null;
        window.calendar.selectedTime = null;
        document.getElementById('horariosContainer').style.display = 'none';
        document.getElementById('btnConfirmar').disabled = true;
        
        // Remove selections
        document.querySelectorAll('.calendar-day.selected').forEach(day => {
            day.classList.remove('selected');
        });
        document.querySelectorAll('.horario-slot.selected').forEach(slot => {
            slot.classList.remove('selected');
        });
    }
    
    // Clear error messages
    document.querySelectorAll('.error-message').forEach(error => {
        error.textContent = '';
    });
}

// Success modal close handler
document.addEventListener('DOMContentLoaded', function() {
    const successModal = document.getElementById('successModal');
    if (successModal) {
        successModal.addEventListener('click', function(e) {
            if (e.target === successModal || e.target.classList.contains('btn')) {
                closeModal('successModal');
                // Redirect to home page
                window.location.href = '/';
            }
        });
    }
});

// Make functions global
window.nextStep = nextStep;
window.prevStep = prevStep;

