function initActivityChart() {
    const ctx = document.getElementById('activity-chart')?.getContext('2d');
    if (!ctx) return;

    const activityData = {
        labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
        datasets: [{
            label: 'Количество мероприятий',
            data: [8, 12, 15, 10, 13, 9],
            backgroundColor: 'rgba(52, 152, 219, 0.2)',
            borderColor: 'rgba(52, 152, 219, 1)',
            borderWidth: 2,
            tension: 0.3
        }]
    };

    const config = {
        type: 'line',
        data: activityData,
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Мероприятий: ${context.parsed.y}`;
                        }
                    }
                }
            },
            scales: {
                y: { beginAtZero: true, ticks: { stepSize: 5 } }
            }
        }
    };

    new Chart(ctx, config);
}

function downloadReport(employeeName, employeeData) {
    alert(`Будет сгенерирован и скачан PDF-отчет для сотрудника: ${employeeName}`);
    console.log('Данные для отчета:', employeeData);
}

function setupEventForm() {
    const form = document.getElementById('create-event-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const eventData = {
                name: formData.get('Название мероприятия'),
                date: formData.get('date'),
                organizer: formData.get('Организатор'),
                description: formData.get('Описание мероприятия'),
                points: parseInt(formData.get('Количество баллов')),
                category: formData.get('Выберите категорию')
            };
            console.log('Новое мероприятие:', eventData);
            alert('Мероприятие успешно создано!');
            form.reset();
        });
    }
}

function setupModerationButtons() {
    const approveButtons = document.querySelectorAll('.approve');
    const rejectButtons = document.querySelectorAll('.reject');
    
    approveButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Вы действительно хотите одобрить этого организатора?')) {
                alert('Организатор одобрен!');
                this.closest('tr').remove();
            }
        });
    });
    
    rejectButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Вы действительно хотите отклонить этого организатора?')) {
                alert('Организатор отклонен!');
                this.closest('tr').remove();
            }
        });
    });
}

function setupDownloadButtons() {
    const downloadButtons = document.querySelectorAll('.download-report');
    
    downloadButtons.forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr');
            const employeeName = row.cells[0].textContent;
            const employeeData = {
                city: row.cells[1].textContent,
                age: parseInt(row.cells[2].textContent),
                events: parseInt(row.cells[3].textContent),
                avgScore: parseFloat(row.cells[4].textContent)
            };
            downloadReport(employeeName, employeeData);
        });
    });
}

function setupWeightsForm() {
    const form = document.getElementById('weights-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const weights = {};
            const inputs = form.querySelectorAll('input[type="number"]');
            inputs.forEach(input => {
                const label = input.previousElementSibling.textContent.replace(':', '').trim();
                weights[label] = parseInt(input.value);
            });
            console.log('Настройки весов:', weights);
            alert('Настройки весов успешно сохранены!');
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('activity-chart')) {
        initActivityChart();
    }
    setupEventForm();
    setupModerationButtons();
    setupDownloadButtons();
    setupWeightsForm();
});
