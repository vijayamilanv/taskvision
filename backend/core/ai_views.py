import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
import os

# Initialize Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'your-api-key-here'))

class AIChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message')
        context = request.data.get('context', {})
        
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = genai.GenerativeModel('gemini-pro')
            
            # Construct a rich, role-specific system prompt
            role = getattr(request.user, 'role', 'TM')
            role_description = {
                'PO': "You are the TaskVision Strategic Advisor. Focus on project vision, ROI, and high-level milestones. Help refine project scope and stakeholder alignment.",
                'PM': "You are the TaskVision Operations Expert. Focus on task distribution, deadline risks, and team capacity. Spot potential bottlenecks early.",
                'TM': "You are the TaskVision Technical Partner. Focus on task completion, blocker resolution, and efficient execution. Help break down Jira-style tasks into steps."
            }.get(role, "You are the TaskVision AI Assistant.")

            system_prompt = f"{role_description} User: {request.user.get_full_name() or request.user.username}. "
            
            if context:
                system_prompt += (
                    f"WORKSPACE CONTEXT: {context.get('totalProjects', 0)} Active projects, "
                    f"{context.get('totalTasks', 0)} Assignments. "
                    f"Current focus: {context.get('currentTab', 'Dashboard')}. "
                )

            full_prompt = f"{system_prompt}\nUser: {user_message}\nAI Advisor:"
            
            response = model.generate_content(full_prompt)
            return Response({'reply': response.text, 'status': 'success'})
            
        except Exception as e:
            # Enhanced mock response for fallback
            role = getattr(request.user, 'role', 'TM')
            fallback_replies = {
                'PO': f"Strategic Insight: Based on your {context.get('totalProjects', 0)} projects, I recommend focusing on clear milestone definition this week.",
                'PM': f"Operations Tip: You have {context.get('totalTasks', 'some')} tasks across your team. Ensure high-priority items have assigned owners.",
                'TM': f"Execution Focus: I see your active assignments. Try knocking out the 'Todo' items with the earliest deadlines first."
            }
            return Response({
                'reply': fallback_replies.get(role, "I'm currently in lightweight mode. How can I help you with your tasks?"),
                'status': 'fallback',
                'debug': str(e)
            })
