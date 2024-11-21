import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: "light", // 기본 테마 설정
    themes: {
      light: {
        colors: {
          primary: "#1557B0", // 주요 색상 (파란색)
          secondary: "#F3F4F6", // 보조 색상 (연한 회색)
          background: "#FFFFFF", // 배경색
          accent: "#FFD700", // 강조 색상 (금색)
          error: "#FF5252", // 에러 색상
          info: "#2196F3", // 정보 색상
          success: "#4CAF50", // 성공 색상
          warning: "#FFC107", // 경고 색상
        },
      },
    },
  },
});
