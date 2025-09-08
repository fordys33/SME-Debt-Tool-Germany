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
            case 'funding-guidance':
                if ('funding-guidance' === 'debt-brake') {
                    result = {
                        debt_limit: data.revenue * 0.0035,
                        available_capacity: Math.max(0, (data.revenue * 0.0035) - data.currentDebt),
                        debt_usage: data.currentDebt > 0 ? (data.currentDebt / (data.revenue * 0.0035)) * 100 : 0,
                        status: 'Within Limits',
                        status_class: 'bg-success'
                    };
                } else if ('funding-guidance' === 'cost-analysis') {
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
                } else if ('funding-guidance' === 'debt-equity') {
                    const newShares = Math.round(data.debtAmount / data.sharePrice);
                    const totalShares = data.existingShares + newShares;
                    const ownershipDilution = (newShares / totalShares) * 100;
                    result = {
                        new_shares_issued: newShares,
                        total_shares_after: totalShares,
                        new_share_price: data.sharePrice,
                        ownership_dilution: ownershipDilution,
                        debt_reduction: data.debtAmount,
                        impact: ownershipDilution > 20 ? 'High dilution - consider alternative' : 'Acceptable dilution'
                    };
                } else if ('funding-guidance' === 'debt-snowball') {
                    // Sort debts by interest rate (highest first)
                    const sortedDebts = data.debts.sort((a, b) => b.interestRate - a.interestRate);
                    let totalInterest = 0;
                    let totalPaid = 0;
                    let months = 0;
                    
                    for (const debt of sortedDebts) {
                        const monthlyRate = debt.interestRate / 100 / 12;
                        const numPayments = Math.log(1 + (debt.balance * monthlyRate) / data.monthlyPayment) / Math.log(1 + monthlyRate);
                        const interest = (data.monthlyPayment * numPayments) - debt.balance;
                        totalInterest += interest;
                        totalPaid += debt.balance + interest;
                        months += numPayments;
                    }
                    
                    result = {
                        total_interest: totalInterest,
                        total_paid: totalPaid,
                        total_months: months,
                        monthly_payment: data.monthlyPayment,
                        strategy: 'Pay highest interest first'
                    };
                } else if ('funding-guidance' === 'funding-guidance') {
                    result = {
                        recommended_programs: ['Innovation Funding', 'Green Transition Support', 'Digital Transformation Grant'],
                        estimated_amount: data.revenue * 0.05,
                        application_time: '2-6 months',
                        success_rate: '65%'
                    };
                } else if ('funding-guidance' === 'covenant-tracking') {
                    const debtToEbitda = data.totalDebt / data.ebitda;
                    const interestCoverage = data.ebitda / data.interestExpense;
                    const debtToAssets = data.totalDebt / data.totalAssets;
                    const cashFlowCoverage = data.operatingCashFlow / data.debtService;
                    
                    result = {
                        debt_to_ebitda: debtToEbitda,
                        interest_coverage: interestCoverage,
                        debt_to_assets: debtToAssets,
                        cash_flow_coverage: cashFlowCoverage,
                        overall_status: (debtToEbitda < 3 && interestCoverage > 3) ? 'Compliant' : 'At Risk'
                    };
                }
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
