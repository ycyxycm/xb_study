import {request} from "./request";
import api from "./api";

var myfunction={
  check_session(dom){
    request.get(api.http+"/check/session").then(res => {
      if(res.data.status==-1){
        dom.$notify.error({
          title: '错误',
          message: res.data.msg
        });
        dom.$router.push({path:'/login'})
        return false
      }else {
        return true
      }
    });
  }
}


export default myfunction;
