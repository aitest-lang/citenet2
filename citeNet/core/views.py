from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from .models import History
from django.db.models import Q

@login_required() #redirect when user is not logged in
def search(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
    }
    return render(request,"core/search_suggestions.html",context)

@csrf_exempt
def save_search(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            search_id = data.get('id')
            if search_id is not None:
                request.session['search_id'] = search_id
                return JsonResponse({'status': 'success', 'message': 'Search ID saved successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid search ID'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required()
def tree(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
    }
    
    search_id = request.session.get('search_id', None)
    
    if search_id:
        context['search_id'] = search_id
        request.session.pop('search_id', None)
    return render(request, "core/tree.html", context)

@csrf_exempt
def save_history(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user = request.user
            if history is not None and user.is_authenticated:
                History.objects.create(
                    user=user,
                    history=data  # Directly assign the JSON data to the JSONField
                )
                return JsonResponse({'status': 'success', 'message': 'History saved successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid history'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



@login_required
def history(request):
    # Get the currently logged-in user
    user = request.user

    # Query all history entries for the user, ordered by timestamp (newest first)
    user_history = History.objects.filter(user=user).order_by('-timestamp')

    # Prepare the history data for the template
    history_data = []
    for entry in user_history:
        try:
            # Since `history` is already a JSONField, no need to use `json.loads`
            decoded_history = entry.history['nodes'][0]['title']
            # print(decoded_history['nodes'][0]['title']) # This is already a Python dictionary

            history_data.append({
                'id': entry.id,
                'history': decoded_history,
                'timestamp': entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Format the timestamp
            })
        except Exception as e:
            # Log any errors that occur during processing
            print(f"Error processing history entry {entry.id}: {e}")

    # Pass the processed data to the template
    context = {
        'history_data': history_data,
    }
    return render(request, "core/history.html", context)  # Ensure you have a template "core/history.html"

@login_required
def history_detail(request, pk):
    # Get ONLY the 'history' field for the current user's entry
    history_data = get_object_or_404(
        History.objects.filter(user=request.user).values('history'),
        pk=pk
    )

    data = history_data["history"]
    
    return JsonResponse(data, safe=False)

@login_required
def specific_tree(request, pk):    
    return render(request, "core/history_tree.html", {'pk': pk})

@login_required  # Ensures only authenticated users can access this view
def delete_history(request, id):
    if request.method == "POST":
        history_entry = get_object_or_404(
        History.objects.filter(user=request.user),
        pk=id)
        
        # Check if the session user (request.user) is the owner of the entry
        if history_entry.user != request.user:
            return HttpResponseForbidden("You don't own this history entry.")
        
        history_entry.delete()
    
    return redirect("history")