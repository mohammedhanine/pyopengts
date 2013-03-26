from twisted.web import resource


class RESETQuoter(resource.Resource):
    isLeaf=True
    def render_GET(self,request):
        return 'hellooooooooo'
