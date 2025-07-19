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
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: #333;
                position: relative;
                overflow-x: hidden;
            }
            
            .welcome-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 60px 80px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 700px;
                margin: 20px;
                animation: fadeInUp 0.8s ease-out;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .welcome-message h1 {
                font-size: 2.5em;
                margin-bottom: 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 700;
            }
            
            .welcome-message p {
                font-size: 1.2em;
                margin-bottom: 20px;
                color: #555;
                line-height: 1.6;
            }
            
            .welcome-message a {
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
                position: relative;
            }
            
            .welcome-message a:hover {
                color: #764ba2;
                transform: translateY(-2px);
            }
            
            .welcome-message a::after {
                content: '';
                position: absolute;
                width: 0;
                height: 2px;
                bottom: -2px;
                left: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                transition: width 0.3s ease;
            }
            
            .welcome-message a:hover::after {
                width: 100%;
            }
            
            .small-text {
                font-size: 1em;
                color: #777;
                margin-top: 30px;
            }
            
            .feature-grid {
                display: flex;
                justify-content: space-between;
                gap: 20px;
                margin: 30px 0;
                width: 100%;
            }
            
            .feature-item {
                background: rgba(102, 126, 234, 0.1);
                border-radius: 10px;
                padding: 20px;
                transition: transform 0.3s ease;
                flex: 1;
                min-width: 0;
            }
            
            .feature-item:hover {
                transform: translateY(-5px);
            }
            
            .feature-icon {
                font-size: 2em;
                margin-bottom: 10px;
            }
            
            footer {
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                padding: 20px 0;
                text-align: center;
                color: white;
                font-size: 1.1em;
            }
            
            footer a {
                color: #fff;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            footer a:hover {
                color: #ffeb3b;
                text-shadow: 0 0 10px rgba(255, 235, 59, 0.5);
            }
            
            @media (max-width: 600px) {
                .welcome-container {
                    padding: 40px 30px;
                    margin: 15px;
                }
                
                .welcome-message h1 {
                    font-size: 2em;
                }
                
                .welcome-message p {
                    font-size: 1.1em;
                }
                
                .feature-grid {
                    flex-direction: column;
                    gap: 15px;
                }
            }
        </style>
    </head>
    <body>
        <div class="welcome-container">
            <div class="welcome-message">
                <h1>🎉 Welcome to Heimdallr! 🎉</h1>
                <p>部署成功！您的通知服务已经就绪</p>
                
                <div class="feature-grid">
                    <div class="feature-item">
                        <div class="feature-icon">📱</div>
                        <p>多平台通知</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">⚡</div>
                        <p>快速部署</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🔧</div>
                        <p>易于集成</p>
                    </div>
                </div>
                
                <p><a href="/docs">查看接口文档</a> 开始使用</p>
                <p class="small-text">不知道怎么用？查看<a href="https://github.com/LeslieLeung/heimdallr#%E7%A4%BA%E4%BE%8B%E5%BA%94%E7%94%A8" target="_blank">示例应用</a></p>
            </div>
        </div>
        <footer>
            <p>⭐ 如果觉得本项目不错，不妨给个Star！ <a href="https://github.com/leslieleung/heimdallr" target="_blank">GitHub</a></p>
        </footer>
    </body>
    </html>
    """
