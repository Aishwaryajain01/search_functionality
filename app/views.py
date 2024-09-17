from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from rapidfuzz import process, fuzz
from .models import MedicalTerm, SelectedSuggestion
from django.http import HttpResponseNotFound


# Helper Function:
def get_suggestions(user_input, limit=10, threshold=85):
    # Normalize user input for case-insensitive matching
    user_input = user_input.lower()

    # Fetch all preferred terms from the database
    terms_list = list(MedicalTerm.objects.values_list('tree_number', flat=True))

    # Get suggestions based on prefix matching
    prefix_matches = MedicalTerm.objects.filter(tree_number__istartswith=user_input).values_list('tree_number', flat=True)
    
    # If not enough prefix matches, continue with fuzzy matching
    if len(prefix_matches) < limit:
        fuzzy_suggestions = process.extract(user_input, terms_list, limit=limit, scorer=fuzz.ratio)
        filtered_fuzzy_suggestions = [suggestion[0] for suggestion in fuzzy_suggestions if suggestion[1] >= threshold]

        # Combine prefix matches with filtered fuzzy suggestions, removing duplicates
        combined_suggestions = set(prefix_matches) | set(filtered_fuzzy_suggestions)
    else:
        combined_suggestions = prefix_matches

    # Sort and limit the combined suggestions
    suggestions = sorted(combined_suggestions)[:limit]
    
    # Return the limited medical terms (filter if needed)
    return suggestions[:limit]

# Function for Suggested Terms Symptoms and Diagnosis:
@csrf_exempt
@require_http_methods(["POST"])
def suggest_terms(request):
    user_input = request.POST.get('user_input', '')
    if user_input:
        suggestions = get_suggestions(user_input)
        
        if not suggestions:
            return JsonResponse({'error': f"No close matches found for '{user_input}' in the database."}, status=404)
        
        return JsonResponse({'suggestions': suggestions})
    else:
        return JsonResponse({'error': 'No input provided'}, status=400)
    

@csrf_exempt
@require_http_methods(["POST"])

def save_suggestion(request):
    term = request.POST.get('term')
    print("******",term)
    try:
        term_instance = MedicalTerm.objects.get(tree_number=term)
    except MedicalTerm.DoesNotExist:
        return JsonResponse({"error": "Medical term not found"}, status=404)
    
    SelectedSuggestion.objects.create(data=term_instance)
    return JsonResponse({"status": "success"})