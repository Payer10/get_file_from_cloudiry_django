from rest_framework.decorators import api_view
from rest_framework.response import Response
from cloudinary import Search

@api_view(['GET'])
def get_random_media(request):
    """
    Fetch specific image/video from Cloudinary
    Query params:
      - public_id: (optional) specific media id
      - type: image|video (default=image)
      - prefix: (optional) fetch all media starting with this folder/prefix
      - tag: (optional) fetch media with this tag
    """
    media_type = request.GET.get("type", "video")
    public_id = request.GET.get("public_id")
    prefix = request.GET.get("prefix")
    tag = request.GET.get("tag")

    try:
        if public_id:
            # Specific media by public_id
            from cloudinary import CloudinaryResource
            url = CloudinaryResource(public_id, resource_type=media_type).build_url()
            return Response({"ok": True, "public_id": public_id, "url": url, "resource_type": media_type})

        # Otherwise use search with prefix/tag
        expr = f"resource_type:{media_type}"
        if prefix:
            expr += f' AND public_id STARTS_WITH "{prefix}"'
        if tag:
            expr += f' AND tags:{tag}'

        result = Search().expression(expr).max_results(100).execute()
        resources = result.get("resources", [])
        if not resources:
            return Response({"ok": False, "error": "No media found"}, status=404)

        # Return all matching media
        media_list = []
        for r in resources:
            media_list.append({
                "public_id": r["public_id"],
                "url": r["secure_url"],
                "resource_type": r["resource_type"],
                "format": r.get("format"),
                "width": r.get("width"),
                "height": r.get("height"),
            })

        return Response({"ok": True, "count": len(media_list), "media": media_list})

    except Exception as e:
        return Response({"ok": False, "error": str(e)}, status=500)
