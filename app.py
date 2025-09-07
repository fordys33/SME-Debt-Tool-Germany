import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Use ProxyFix for production deployment
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Custom translation function
    def _(text):
        """Simple translation function"""
        if session.get('language', 'de') == 'de':
            translations = {
                # Navigation
                'SME Debt Management Tool - Germany': 'SME-Schuldenmanagement-Tool - Deutschland',
                'SME Debt Tool': 'SME-Schulden-Tool',
                'Debt Brake': 'Schuldenbremse',
                'Cost Analysis': 'Kostenanalyse',
                'Debt-Equity Swap': 'Schulden-Eigenkapital-Tausch',
                'Debt Snowball': 'Schulden-Schneeball',
                'Funding': 'Finanzierung',
                'Covenants': 'Covenants',
                'About': 'Über',
                'Support': 'Unterstützung',
                'Language': 'Sprache',
                'Switch to German': 'Zu Deutsch wechseln',
                
                # Common terms
                'Calculate': 'Berechnen',
                'Reset': 'Zurücksetzen',
                'Results': 'Ergebnisse',
                'Information': 'Information',
                'Warning': 'Warnung',
                'Success': 'Erfolg',
                'Error': 'Fehler',
                'Amount': 'Betrag',
                'Interest Rate': 'Zinssatz',
                'Term': 'Laufzeit',
                'Monthly Payment': 'Monatliche Zahlung',
                'Total Interest': 'Gesamtzinsen',
                'Total Amount': 'Gesamtbetrag',
                
                # Homepage
                'Comprehensive debt management solutions for German SMEs': 'Umfassende Schuldenmanagement-Lösungen für deutsche KMU',
                'Calculate debt limits, analyze costs, prioritize repayments, and find funding opportunities': 'Berechnen Sie Schuldengrenzen, analysieren Sie Kosten, priorisieren Sie Rückzahlungen und finden Sie Finanzierungsmöglichkeiten',
                'Get Started': 'Loslegen',
                'Learn More': 'Mehr erfahren',
                
                # Features
                'Debt Brake Calculator': 'Schuldenbremse-Rechner',
                'Calculate maximum sustainable debt levels': 'Berechnen Sie maximale nachhaltige Schuldenniveaus',
                'Cost of Debt Analysis': 'Schuldenkosten-Analyse',
                'Analyze total cost of borrowing': 'Analysieren Sie die Gesamtkosten der Kreditaufnahme',
                'Debt-for-Equity Swap Simulation': 'Schulden-Eigenkapital-Tausch-Simulation',
                'Simulate debt restructuring scenarios': 'Simulieren Sie Schuldenrestrukturierungsszenarien',
                'Debt Snowball Prioritization': 'Schulden-Schneeball-Priorisierung',
                'Optimize debt repayment strategy': 'Optimieren Sie die Schuldenrückzahlungsstrategie',
                'EU/Federal Funding Guidance': 'EU/Bundesfinanzierungsberatung',
                'Find available funding programs': 'Finden Sie verfügbare Finanzierungsprogramme',
                'Debt Covenant Tracking': 'Schulden-Covenant-Verfolgung',
                'Monitor debt agreement compliance': 'Überwachen Sie die Einhaltung von Schuldenvereinbarungen',
                
                # Footer
                'This tool is for educational purposes only. Consult financial professionals for advice.': 'Dieses Tool dient nur zu Bildungszwecken. Konsultieren Sie Finanzexperten für Beratung.',
                'Built with Flask & Bootstrap': 'Erstellt mit Flask & Bootstrap',
                'Privacy Policy': 'Datenschutzrichtlinie',
                'Terms of Service': 'Nutzungsbedingungen',
                
                # Donation page
                'Support Development': 'Entwicklung unterstützen',
                'Help us continue building tools for Germany': 'Helfen Sie uns, weiterhin Tools für Deutschland zu entwickeln',
                'Your friendly American citizen building bipartisan tools for Germany': 'Ihr freundlicher amerikanischer Bürger, der parteiübergreifende Tools für Deutschland entwickelt',
                'Donate via PayPal': 'Spenden Sie über PayPal',
                'Buy Me a Coffee': 'Kaufen Sie mir einen Kaffee',
                'Every contribution helps us maintain and improve these tools': 'Jeder Beitrag hilft uns, diese Tools zu erhalten und zu verbessern',
                'Thank you for your support!': 'Vielen Dank für Ihre Unterstützung!',
                
                # Error pages
                'Page Not Found': 'Seite nicht gefunden',
                'The page you are looking for does not exist.': 'Die gesuchte Seite existiert nicht.',
                'Go Home': 'Zur Startseite',
                'Internal Server Error': 'Interner Serverfehler',
                'Something went wrong on our end.': 'Etwas ist auf unserer Seite schief gelaufen.',
                'Try Again': 'Erneut versuchen',
                
                # Debt Brake Calculator
                'Annual Revenue': 'Jahresumsatz',
                'Annual Expenses': 'Jahresausgaben',
                'Existing Debt': 'Bestehende Schulden',
                'Max Debt Service Ratio': 'Maximales Schuldendienstverhältnis',
                'Your total annual revenue': 'Ihr gesamter Jahresumsatz',
                'Your total annual expenses': 'Ihre gesamten Jahresausgaben',
                'Current outstanding debt': 'Aktuelle ausstehende Schulden',
                'Maximum percentage of net income for debt service': 'Maximaler Prozentsatz des Nettoeinkommens für Schuldendienst',
                'Calculate the maximum sustainable debt level for your SME based on income and expenses.': 'Berechnen Sie das maximale nachhaltige Schuldenniveau für Ihr KMU basierend auf Einkommen und Ausgaben.',
                'How It Works': 'Wie es funktioniert',
                'The Debt Brake Calculator helps you determine the maximum sustainable debt level for your business.': 'Der Schuldenbremse-Rechner hilft Ihnen, das maximale nachhaltige Schuldenniveau für Ihr Unternehmen zu bestimmen.',
                'Calculation Method:': 'Berechnungsmethode:',
                'Calculate net income (Revenue - Expenses)': 'Nettoeinkommen berechnen (Umsatz - Ausgaben)',
                'Determine maximum debt service (Net Income × Ratio)': 'Maximalen Schuldendienst bestimmen (Nettoeinkommen × Verhältnis)',
                'Calculate maximum new debt capacity': 'Maximale neue Schuldenkapazität berechnen',
                'Assess current debt-to-income ratio': 'Aktuelles Schulden-zu-Einkommen-Verhältnis bewerten',
                'Tip:': 'Tipp:',
                'A debt service ratio of 30% is generally considered safe for most businesses.': 'Ein Schuldendienstverhältnis von 30% wird für die meisten Unternehmen als sicher angesehen.',
                'Important Notes': 'Wichtige Hinweise',
                'This is a simplified calculation': 'Dies ist eine vereinfachte Berechnung',
                'Consider seasonal variations in income': 'Berücksichtigen Sie saisonale Einkommensschwankungen',
                'Account for emergency reserves': 'Berücksichtigen Sie Notfallreserven',
                'Consult with financial advisors': 'Konsultieren Sie Finanzberater',
                
                # Cost Analysis
                'Loan Amount': 'Darlehensbetrag',
                'Annual Interest Rate': 'Jährlicher Zinssatz',
                'Loan Term': 'Darlehenslaufzeit',
                'Upfront Fees': 'Vorabgebühren',
                'Monthly Fees': 'Monatliche Gebühren',
                'Opportunity Cost Rate': 'Opportunitätskostensatz',
                'Total amount borrowed': 'Gesamtbetrag des Darlehens',
                'Annual percentage rate': 'Jährlicher Prozentsatz',
                'Repayment period': 'Rückzahlungszeitraum',
                'Processing fees, origination fees, etc.': 'Bearbeitungsgebühren, Darlehensgebühren usw.',
                'Account maintenance fees': 'Kontoführungsgebühren',
                'Alternative investment return rate': 'Alternative Anlagerendite',
                'Analyze the total cost of borrowing including interest, fees, and opportunity costs.': 'Analysieren Sie die Gesamtkosten der Kreditaufnahme einschließlich Zinsen, Gebühren und Opportunitätskosten.',
                'Cost Components': 'Kostenelemente',
                'The total cost of debt includes several components:': 'Die Gesamtkosten der Schulden umfassen mehrere Komponenten:',
                'Interest Costs': 'Zinskosten',
                'The primary cost of borrowing money': 'Die Hauptkosten der Kreditaufnahme',
                'Fees': 'Gebühren',
                'Upfront and ongoing fees charged by the lender': 'Vorab- und laufende Gebühren des Kreditgebers',
                'Opportunity Cost': 'Opportunitätskosten',
                'Potential returns from alternative investments': 'Potenzielle Renditen aus alternativen Investitionen',
                'Compare different loan options to find the most cost-effective solution.': 'Vergleichen Sie verschiedene Darlehensoptionen, um die kosteneffektivste Lösung zu finden.',
                'Rates may vary based on creditworthiness': 'Zinssätze können je nach Bonität variieren',
                'Consider tax implications of interest': 'Berücksichtigen Sie steuerliche Auswirkungen von Zinsen',
                'Factor in inflation effects': 'Berücksichtigen Sie Inflationsauswirkungen',
                'Review all loan terms carefully': 'Überprüfen Sie alle Darlehensbedingungen sorgfältig'
            }
            return translations.get(text, text)
        return text
    
    # Make translation function available in templates
    app.jinja_env.globals.update(_=_)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/debt-brake')
    def debt_brake():
        return render_template('debt_brake.html')
    
    @app.route('/cost-analysis')
    def cost_analysis():
        return render_template('cost_analysis.html')
    
    @app.route('/debt-equity')
    def debt_equity():
        return render_template('debt_equity.html')
    
    @app.route('/debt-snowball')
    def debt_snowball():
        return render_template('debt_snowball.html')
    
    @app.route('/funding-guidance')
    def funding_guidance():
        return render_template('funding_guidance.html')
    
    @app.route('/covenant-tracking')
    def covenant_tracking():
        return render_template('covenant_tracking.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/donation')
    def donation():
        return render_template('donation.html')
    
    # Language switching route
    @app.route('/set-language/<lang>')
    def set_language(lang):
        if lang in ['en', 'de']:
            session['language'] = lang
        return redirect(request.referrer or url_for('index'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)