from fastapi import APIRouter
from fastapi.responses import HTMLResponse

welcome_router = APIRouter()


@welcome_router.get("/", response_class=HTMLResponse)
async def welcome():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to Heimdallr!</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .welcome-message {
                text-align: center;
                font-size: 2em;
                color: #333;
            }
            .small-text {
                color: #666;
                font-size: 0.8em;
            }
            footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #666; /* Changed the color here */
                color: white;
                text-align: center;
                padding: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="welcome-message">
            <h1>🎉Welcome to Heimdallr!🎉</h1>
            <p>部署成功！查看<a href="/docs">接口文档</a></p>
            <p class="small-text">不知道怎么用？查看<a href="https://github.com/LeslieLeung/heimdallr#%E7%A4%BA%E4%BE%8B%E5%BA%94%E7%94%A8" target="_blank">示例应用</a></p>
        </div>
        <footer>
            <p>如果觉得本项目不错，不妨给个Star！<a href="https://github.com/leslieleung/heimdallr" target="_blank">GitHub</a></p>
        </footer>
    </body>
    </html>
    """
