anime({
  targets: '.row svg',
  translateY: 10,
  autoplay: true,
  loop: true,
  easing: 'easeInOutSine',
  direction: 'alternate'
});

// 设置“龟”字的动画
const turtleAnimation = anime({
  targets: '#character text',
  opacity: [0, 1],
  duration: 3500,
  delay: 80,
  autoplay: true,
  loop: true,
});

// 设置刀的动画
const knifeAnimation = anime({
  targets: '#icon path',
  opacity: [1, 0],
  duration: 3500,
  delay: 80,
  autoplay: true,
  loop: true,
});


