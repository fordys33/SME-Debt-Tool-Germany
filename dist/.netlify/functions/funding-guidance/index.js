const { Handler } = require('@netlify/functions');

exports.handler = Handler(async (event, context) => {
    // Handle CORS
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const data = JSON.parse(event.body);
        
        // Mock calculation logic (replace with actual calculations)
        let result = {};
        
        switch ('funding-guidance') {
            case 'debt-brake':
                result = {
                    debt_limit: data.revenue * 0.0035,
                    available_capacity: Math.max(0, (data.revenue * 0.0035) - data.currentDebt),
                    debt_usage: data.currentDebt > 0 ? (data.currentDebt / (data.revenue * 0.0035)) * 100 : 0,
                    status: 'Within Limits',
                    status_class: 'bg-success'
                };
                break;
            case 'cost-analysis':
                const monthlyRate = data.interestRate / 100 / 12;
                const numPayments = data.term * 12;
                const monthlyPayment = data.principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / (Math.pow(1 + monthlyRate, numPayments) - 1);
                result = {
                    monthly_payment: monthlyPayment,
                    total_payment: monthlyPayment * numPayments,
                    total_interest: (monthlyPayment * numPayments) - data.principal,
                    after_tax_interest: ((monthlyPayment * numPayments) - data.principal) * (1 - data.taxRate / 100),
                    effective_rate: data.interestRate * (1 - data.taxRate / 100)
                };
                break;
            default:
                result = { message: 'Function not implemented yet' };
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify(result)
        };
        
    } catch (error) {
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Internal server error' })
        };
    }
});
