from rest_framework.decorators import api_view
from rest_framework.response import Response
from cloudinary import Search

@api_view(['GET'])
def get_random_media(request):

    media_type = request.GET.get("type", None) 

    try:
        result = (
            Search()
            .expression(f"resource_type:{media_type}")
            .max_results(100)
            .execute() 
        )
        resources = result.get("resources", [])
        if not resources:
            return Response({"ok": False, "error": f"No {media_type} found"}, status=404)

        data = []
        for res in resources:
            data.append({
                "public_id": res["public_id"],
                "url": res["secure_url"],
                "resource_type": res["resource_type"],
                "format": res.get("format"),
                "width": res.get("width"),
                "height": res.get("height"),
            })

        return Response({"ok": True, "count": len(data), "results": data})

    except Exception as e:
        return Response({"ok": False, "error": str(e)}, status=500)
