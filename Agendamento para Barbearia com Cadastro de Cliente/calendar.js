// Calendar functionality for Barbearia Clássica

class Calendar {
    constructor() {
        this.currentDate = new Date();
        this.selectedDate = null;
        this.selectedTime = null;
        this.availableTimes = [
            '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
            '14:00', '14:30', '15:00', '15:30', '16:00', '16:30',
            '17:00', '17:30', '18:00', '18:30'
        ];
        this.weekendTimes = [
            '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
            '11:00', '11:30', '14:00', '14:30', '15:00', '15:30',
            '16:00', '16:30'
        ];
        this.init();
    }

    init() {
        this.renderCalendar();
        this.bindEvents();
    }

    bindEvents() {
        document.getElementById('prevMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.renderCalendar();
        });

        document.getElementById('nextMonth').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.renderCalendar();
        });
    }

    renderCalendar() {
        const calendar = document.getElementById('calendar');
        const currentMonth = document.getElementById('currentMonth');
        
        // Clear calendar
        calendar.innerHTML = '';
        
        // Set month header
        const monthNames = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ];
        currentMonth.textContent = `${monthNames[this.currentDate.getMonth()]} ${this.currentDate.getFullYear()}`;
        
        // Add day headers
        const dayHeaders = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
        dayHeaders.forEach(day => {
            const dayHeader = document.createElement('div');
            dayHeader.className = 'calendar-day-header';
            dayHeader.textContent = day;
            calendar.appendChild(dayHeader);
        });
        
        // Get first day of month and number of days
        const firstDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), 1);
        const lastDay = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();
        
        // Add empty cells for days before month starts
        for (let i = 0; i < startingDayOfWeek; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day other-month';
            calendar.appendChild(emptyDay);
        }
        
        // Add days of the month
        const today = new Date();
        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = day;
            
            const currentDayDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth(), day);
            
            // Check if it's today
            if (this.isSameDay(currentDayDate, today)) {
                dayElement.classList.add('today');
            }
            
            // Check if it's available (not Sunday and not in the past)
            if (this.isAvailableDate(currentDayDate)) {
                dayElement.classList.add('available');
                dayElement.addEventListener('click', () => {
                    this.selectDate(currentDayDate, dayElement);
                });
            } else {
                dayElement.classList.add('disabled');
            }
            
            calendar.appendChild(dayElement);
        }
    }

    isAvailableDate(date) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        // Not available if it's in the past
        if (date < today) return false;
        
        // Not available on Sundays (0 = Sunday)
        if (date.getDay() === 0) return false;
        
        return true;
    }

    isSameDay(date1, date2) {
        return date1.getDate() === date2.getDate() &&
               date1.getMonth() === date2.getMonth() &&
               date1.getFullYear() === date2.getFullYear();
    }

    selectDate(date, element) {
        // Remove previous selection
        document.querySelectorAll('.calendar-day.selected').forEach(day => {
            day.classList.remove('selected');
        });
        
        // Add selection to clicked day
        element.classList.add('selected');
        this.selectedDate = date;
        
        // Show available times
        this.showAvailableTimes(date);
    }

    showAvailableTimes(date) {
        const container = document.getElementById('horariosContainer');
        const grid = document.getElementById('horariosGrid');
        
        // Clear previous times
        grid.innerHTML = '';
        
        // Determine available times based on day of week
        const dayOfWeek = date.getDay();
        const times = dayOfWeek === 6 ? this.weekendTimes : this.availableTimes; // Saturday = 6
        
        // Create time slots
        times.forEach(time => {
            const timeSlot = document.createElement('div');
            timeSlot.className = 'horario-slot';
            timeSlot.textContent = time;
            
            // Check if time is available (mock logic - in real app, check with backend)
            if (this.isTimeAvailable(date, time)) {
                timeSlot.addEventListener('click', () => {
                    this.selectTime(time, timeSlot);
                });
            } else {
                timeSlot.classList.add('disabled');
            }
            
            grid.appendChild(timeSlot);
        });
        
        // Show the container
        container.style.display = 'block';
        
        // Scroll to times
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    isTimeAvailable(date, time) {
        // Mock logic - in real app, this would check with backend
        // For demo purposes, make some random times unavailable
        const unavailableTimes = ['10:30', '15:00', '17:30'];
        return !unavailableTimes.includes(time);
    }

    selectTime(time, element) {
        // Remove previous selection
        document.querySelectorAll('.horario-slot.selected').forEach(slot => {
            slot.classList.remove('selected');
        });
        
        // Add selection to clicked time
        element.classList.add('selected');
        this.selectedTime = time;
        
        // Enable confirm button
        const btnConfirmar = document.getElementById('btnConfirmar');
        btnConfirmar.disabled = false;
    }

    getSelectedDateTime() {
        if (!this.selectedDate || !this.selectedTime) {
            return null;
        }
        
        return {
            date: this.selectedDate,
            time: this.selectedTime,
            dateString: this.formatDate(this.selectedDate),
            timeString: this.selectedTime
        };
    }

    formatDate(date) {
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        return date.toLocaleDateString('pt-BR', options);
    }
}

// Initialize calendar when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('calendar')) {
        window.calendar = new Calendar();
    }
});

