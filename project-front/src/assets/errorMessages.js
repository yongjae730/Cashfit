export const errorMessages = {
  "A user with that username already exists.": "이미 사용 중인 아이디입니다.",
  "This field may not be blank.": "이 필드는 비워둘 수 없습니다.",
  "Password fields didn't match.": "비밀번호가 일치하지 않습니다.",
  "Ensure this value has at least 8 characters (it has 6).": "비밀번호는 최소 8자 이상이어야 합니다.",
};

export const translateErrorMessage = (message) => {
  return errorMessages[message] || "알 수 없는 오류가 발생했습니다.";
};
