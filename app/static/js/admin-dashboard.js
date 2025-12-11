/**
 * Admin Dashboard JavaScript (Final Corrected Version)
 */

// Toggle to use live API data in dashboard charts. Set to false to use static/mock values.
const ENABLE_LIVE_DASHBOARD_DATA = false;

// Helper function to get text color based on theme
function getTextColor() {
    // Check the admin content background to determine theme
    const adminContent = document.querySelector('.admin-content');
    if (adminContent) {
        const bgColor = window.getComputedStyle(adminContent).getPropertyValue('--color-bg') || 
                       window.getComputedStyle(document.body).backgroundColor;
        
        // Simple check: if background contains 'rgb' and has low values, it's dark
        if (bgColor.includes('rgb')) {
            const rgb = bgColor.match(/\d+/g);
            if (rgb && rgb.length >= 3) {
                const avg = (parseInt(rgb[0]) + parseInt(rgb[1]) + parseInt(rgb[2])) / 3;
                // If average RGB < 100, it's dark mode
                return avg < 100 ? '#ffffff' : '#1e293b';
            }
        }
    }
    
    // Fallback: check for dark-theme class on body
    return document.body.classList.contains('dark-theme') ? '#ffffff' : '#1e293b';
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin Dashboard initialized');
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize all charts
    initDailyUsersSparkline();
    initUserTypeDistributionChart();
    initTestResultChart();
    initAssignmentTrafficChart();
});

// Fetch dashboard statistics (optional AJAX)
async function loadDashboardStats() {
    try {
        const response = await fetch('/admin/api/dashboard');
        const data = await response.json();
        
        if (data.success) {
            updateStatistics(data.statistics);
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

// Update statistics on page
function updateStatistics(stats) {
    const elements = {
        students: document.querySelector('[data-stat="students"]'),
        teachers: document.querySelector('[data-stat="teachers"]'),
        tests: document.querySelector('[data-stat="tests"]'),
        assignments: document.querySelector('[data-stat="assignments"]')
    };
    
    if (elements.students && stats.users) {
        elements.students.textContent = stats.users.total_students;
    }
    if (elements.teachers && stats.users) {
        elements.teachers.textContent = stats.users.total_teachers;
    }
    if (elements.tests) {
        elements.tests.textContent = stats.total_tests;
    }
    if (elements.assignments) {
        elements.assignments.textContent = stats.active_assignments;
    }
}

// --------------------- OVERLAPPING LINE CHART ---------------------
async function initDailyUsersSparkline() {
    const canvas = document.getElementById('dailyUsersSparkline');
    if (!canvas || typeof Chart === 'undefined') return;

    let labels = [];
    let datasets = [];

    if (ENABLE_LIVE_DASHBOARD_DATA) {
        try {
            const resp = await fetch('/admin/api/daily-users');
            if (resp.ok) {
                const data = await resp.json();
                labels = Array.isArray(data.labels) ? data.labels : [];
                datasets = [
                    { label: 'Active Users', data: Array.isArray(data.users) ? data.users : [], borderColor: 'rgba(137, 86, 255, 1)', backgroundColor: 'rgba(137, 86, 255, 0.1)', fill: false, tension: 0.35, borderWidth: 2.5, pointRadius: 0 },
                    { label: 'Tests Taken', data: Array.isArray(data.tests) ? data.tests : [], borderColor: 'rgba(255, 99, 132, 1)', backgroundColor: 'rgba(255, 99, 132, 0.1)', fill: false, tension: 0.35, borderWidth: 2.5, pointRadius: 0 },
                    { label: 'Assignments Submitted', data: Array.isArray(data.assignments) ? data.assignments : [], borderColor: 'rgba(54, 162, 235, 1)', backgroundColor: 'rgba(54, 162, 235, 0.1)', fill: false, tension: 0.35, borderWidth: 2.5, pointRadius: 0 }
                ];
            }
        } catch (e) {
            console.warn('Daily users API unavailable, using fallback overlapping data');
        }
    }

    // Fallback data
    if (labels.length === 0) {
        const now = new Date();
        for (let i = 13; i >= 0; i--) {
            const d = new Date(now);
            d.setDate(now.getDate() - i);
            labels.push(`${d.getMonth() + 1}/${d.getDate()}`);
        }

        const randomWalk = (base) => Array.from({ length: 14 }, (_, i) =>
            base + Math.round(15 * Math.sin(i / 2)) + Math.round(Math.random() * 10)
        );

        datasets = [
            {
                label: 'Active Users',
                data: randomWalk(120),
                borderColor: 'rgba(137, 86, 255, 1)',
                backgroundColor: 'rgba(137, 86, 255, 0.1)',
                fill: false,
                tension: 0.35,
                borderWidth: 2.5,
                pointRadius: 0
            },
            {
                label: 'Tests Taken',
                data: randomWalk(100),
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                fill: false,
                tension: 0.35,
                borderWidth: 2.5,
                pointRadius: 0
            },
            {
                label: 'Assignments Submitted',
                data: randomWalk(80),
                borderColor: 'rgba(54, 162, 235, 1)',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                fill: false,
                tension: 0.35,
                borderWidth: 2.5,
                pointRadius: 0
            }
        ];
    }

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: {
                    display: true,
                    labels: { usePointStyle: true, color: getTextColor(), font: { size: 12, weight: '500' } }
                },
                tooltip: { enabled: true }
            },
            scales: {
                x: { 
                    display: true, 
                    grid: { display: false },
                    ticks: { color: getTextColor(), font: { size: 11 } }
                },
                y: { 
                    display: true, 
                    grid: { color: 'rgba(100, 116, 139, 0.1)' },
                    ticks: { color: getTextColor(), font: { size: 11 } }
                }
            }
        }
    });
}

// --------------------- USER TYPE DISTRIBUTION DONUT ---------------------
async function initUserTypeDistributionChart() {
    const canvas = document.getElementById('userTypeDistributionChart');
    if (!canvas || typeof Chart === 'undefined') return;

    const USER_TYPE_STUDENTS = 'Students';
    const USER_TYPE_TEACHERS = 'Teachers';
    const USER_TYPE_ADMINS = 'Admins';

    const userTypeColors = {
        [USER_TYPE_STUDENTS]: { bg: 'rgba(0, 255, 255, 0.85)', border: 'rgba(0, 255, 255, 1)' },
        [USER_TYPE_TEACHERS]: { bg: 'rgba(0, 255, 100, 0.85)', border: 'rgba(0, 255, 100, 1)' },
        [USER_TYPE_ADMINS]: { bg: 'rgba(255, 165, 0, 0.85)', border: 'rgba(255, 165, 0, 1)' }
    };

    let userTypeData = {
        labels: [USER_TYPE_STUDENTS, USER_TYPE_TEACHERS, USER_TYPE_ADMINS],
        values: [65, 30, 5]
    };

    if (ENABLE_LIVE_DASHBOARD_DATA) {
        try {
            const resp = await fetch('/admin/api/user-type-distribution');
            if (resp.ok) {
                const data = await resp.json();
                if (Array.isArray(data.labels) && Array.isArray(data.values)) {
                    userTypeData = data;
                }
            }
        } catch (e) {
            console.warn('User type distribution API unavailable, using fallback data');
        }
    }

    const backgroundColors = userTypeData.labels.map(label =>
        userTypeColors[label]?.bg || 'rgba(150, 150, 150, 0.85)'
    );
    const borderColors = userTypeData.labels.map(label =>
        userTypeColors[label]?.border || 'rgba(150, 150, 150, 1)'
    );

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: userTypeData.labels,
            datasets: [{
                data: userTypeData.values,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: getTextColor(),
                        usePointStyle: true,
                        padding: 15,
                        font: { size: 12, weight: '500' }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// --------------------- TEST RESULT DONUT ---------------------
async function initTestResultChart() {
    const canvas = document.getElementById('testResultChart');
    if (!canvas || typeof Chart === 'undefined') return;

    const RESULT_PASSED = 'Passed';
    const RESULT_FAILED = 'Failed';
    const RESULT_PENDING = 'Pending';
    const RESULT_IN_PROGRESS = 'In Progress';

    const resultColors = {
        [RESULT_PASSED]: { bg: 'rgba(0, 255, 100, 0.85)', border: 'rgba(0, 255, 100, 1)' },
        [RESULT_FAILED]: { bg: 'rgba(255, 50, 100, 0.85)', border: 'rgba(255, 50, 100, 1)' },
        [RESULT_PENDING]: { bg: 'rgba(255, 255, 0, 0.85)', border: 'rgba(255, 255, 0, 1)' },
        [RESULT_IN_PROGRESS]: { bg: 'rgba(0, 255, 255, 0.85)', border: 'rgba(0, 255, 255, 1)' }
    };

    let resultData = {
        labels: [RESULT_PASSED, RESULT_FAILED, RESULT_PENDING, RESULT_IN_PROGRESS],
        values: [55, 20, 15, 10]
    };

    if (ENABLE_LIVE_DASHBOARD_DATA) {
        try {
            const resp = await fetch('/admin/api/test-results');
            if (resp.ok) {
                const data = await resp.json();
                if (Array.isArray(data.labels) && Array.isArray(data.values)) {
                    resultData = data;
                }
            }
        } catch (e) {
            console.warn('Test results API unavailable, using fallback data');
        }
    }

    const backgroundColors = resultData.labels.map(label =>
        resultColors[label]?.bg || 'rgba(150,150,150,0.85)'
    );
    const borderColors = resultData.labels.map(label =>
        resultColors[label]?.border || 'rgba(150,150,150,1)'
    );

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: resultData.labels,
            datasets: [{
                data: resultData.values,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: { color: getTextColor(), usePointStyle: true, padding: 15, font: { size: 12, weight: '500' } }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// --------------------- ASSIGNMENT TRAFFIC DONUT ---------------------
async function initAssignmentTrafficChart() {
    const canvas = document.getElementById('assignmentTrafficChart');
    if (!canvas || typeof Chart === 'undefined') return;

    const sourceColors = {
        'Direct Link': { bg: 'rgba(137, 86, 255, 0.85)', border: 'rgba(137, 86, 255, 1)' },
        'Email': { bg: 'rgba(255, 165, 0, 0.85)', border: 'rgba(255, 165, 0, 1)' },
        'Dashboard': { bg: 'rgba(0, 255, 255, 0.85)', border: 'rgba(0, 255, 255, 1)' },
        'Mobile App': { bg: 'rgba(0, 255, 100, 0.85)', border: 'rgba(0, 255, 100, 1)' },
        'Other': { bg: 'rgba(255, 50, 100, 0.85)', border: 'rgba(255, 50, 100, 1)' }
    };

    let trafficData = {
        labels: ['Direct Link', 'Email', 'Dashboard', 'Mobile App', 'Other'],
        values: [40, 25, 20, 10, 5]
    };

    if (ENABLE_LIVE_DASHBOARD_DATA) {
        try {
            const resp = await fetch('/admin/api/assignment-traffic');
            if (resp.ok) {
                const data = await resp.json();
                if (Array.isArray(data.labels) && Array.isArray(data.values)) {
                    trafficData = data;
                }
            }
        } catch (e) {
            console.warn('Assignment traffic API unavailable, using fallback data');
        }
    }

    const backgroundColors = trafficData.labels.map(label =>
        sourceColors[label]?.bg || 'rgba(150,150,150,0.85)'
    );
    const borderColors = trafficData.labels.map(label =>
        sourceColors[label]?.border || 'rgba(150,150,150,1)'
    );

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: trafficData.labels,
            datasets: [{
                data: trafficData.values,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: { color: getTextColor(), usePointStyle: true, padding: 15, font: { size: 12, weight: '500' } }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}