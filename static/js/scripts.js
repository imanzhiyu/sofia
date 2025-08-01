/**
 * @FilePath: nature/personal_page/static/js/scripts.js
 * @Author: Joel
 * @Date: 2025-07-30 14:56:53
 * @LastEditTime: 2025-08-01 14:19:10
 * @Description: 小组件
 */

// 地球旋转背景（限制在 .earth-box 容器内）
const canvas = document.getElementById('globeCanvas');
const container = canvas.parentElement;  // 即 .earth-box

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({canvas: canvas, alpha: true});
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(window.devicePixelRatio);

scene.add(new THREE.AmbientLight(0xffffff, 0.6));
const directionalLight = new THREE.DirectionalLight(0xffffff, 1.8);
directionalLight.position.set(3, 2, 5);
scene.add(directionalLight);

const loader = new THREE.TextureLoader();
const texture = loader.load('/static/images/earth.jpg');
const geometry = new THREE.SphereGeometry(2.0, 64, 64);
const material = new THREE.MeshStandardMaterial({map: texture});
const sphere = new THREE.Mesh(geometry, material);
scene.add(sphere);

camera.position.z = 4;

function animate() {
    requestAnimationFrame(animate);
    sphere.rotation.y += 0.005;
    renderer.render(scene, camera);
}

animate();

// 📏 响应容器大小变化（不是全窗口）
window.addEventListener('resize', () => {
    const width = container.clientWidth;
    const height = container.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
});

// 页面运行时间
const createdAt = new Date("2025-08-01T00:00:00");

function updateSiteAge() {
    const now = new Date();
    let diff = Math.floor((now - createdAt) / 1000);
    const days = Math.floor(diff / 86400);
    diff %= 86400;
    const hours = Math.floor(diff / 3600);
    diff %= 3600;
    const minutes = Math.floor(diff / 60);
    const seconds = diff % 60;
    document.getElementById("site-age").innerText = `Created：${days} 天 ${hours} 时 ${minutes} 分 ${seconds} 秒`;
}

setInterval(updateSiteAge, 1000);
updateSiteAge();

// 浏览计数（本地存储模拟）
// const visitKey = "total-visits";
// let count = localStorage.getItem(visitKey);
// count = count ? parseInt(count) + 1 : 1;
// localStorage.setItem(visitKey, count);
// document.getElementById("visit-count").innerText = `总访问次数：${count}`;
