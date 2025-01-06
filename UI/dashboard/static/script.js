document.addEventListener('DOMContentLoaded', () => {
    const regionSelect = document.getElementById('region-select');
    const databaseSelect = document.getElementById('database-select');
    const queryTypeSelect = document.getElementById('query-type-select');
    
    function updateMetrics() {
        const region = regionSelect.value;
        const database = databaseSelect.value;
        const queryType = queryTypeSelect.value;
        
        fetch(`/metrics/${database}/${region}/${queryType}`)
            .then(response => response.json())
            .then(data => {
                // Check for errors
                if (data.error) {
                    console.error(data.error);
                    document.getElementById('metrics-chart').innerHTML = `<p>Error: ${data.error}</p>`;
                    return;
                }
                
                // Render Bar Chart
                const barChartDiv = document.createElement('div');
                barChartDiv.id = 'bar-chart';
                barChartDiv.style.width = '100%';
                barChartDiv.style.height = '400px';
                
                const detailedChartDiv = document.createElement('div');
                detailedChartDiv.id = 'detailed-chart';
                detailedChartDiv.style.width = '100%';
                detailedChartDiv.style.height = '400px';
                
                // Clear previous charts and add new containers
                const chartsContainer = document.getElementById('metrics-chart');
                chartsContainer.innerHTML = '';
                chartsContainer.appendChild(barChartDiv);
                chartsContainer.appendChild(detailedChartDiv);
                
                // Plot charts
                Plotly.newPlot('bar-chart', JSON.parse(data.bar_chart));
                Plotly.newPlot('detailed-chart', JSON.parse(data.detailed_chart));
                
                // Update metrics display
                const metricsHtml = Object.entries(data.metrics)
                    .map(([key, value]) => `
                        <div class="metric-item">
                            <strong>${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}:</strong> 
                            ${value}
                        </div>
                    `)
                    .join('');
                
                document.getElementById('detailed-metrics').innerHTML = `
                    <h3>Detailed Metrics</h3>
                    <div class="metrics-grid">${metricsHtml}</div>
                `;
                
                // Update recommendations
                const recommendationsHtml = data.raw_recommendations.map(rec => `
                    <div class="recommendation-card">
                        <h3>${rec['Content Title']}</h3>
                        <p><strong>Type:</strong> ${rec['Content Type']}</p>
                        <p><strong>Total Views:</strong> ${rec['Total Views']}</p>
                        <p><strong>Total Likes:</strong> ${rec['Total Likes']}</p>
                    </div>
                `).join('');
                
                document.getElementById('recommendations').innerHTML = `
                    <h2>${queryType} Recommendations</h2>
                    ${recommendationsHtml}
                `;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('metrics-chart').innerHTML = `<p>Error fetching data</p>`;
            });
    }
    
    // Add event listeners to all select elements
    regionSelect.addEventListener('change', updateMetrics);
    databaseSelect.addEventListener('change', updateMetrics);
    queryTypeSelect.addEventListener('change', updateMetrics);
    
    // Initial load
    updateMetrics();
});