import './HomePage.css'
import {ChatBox} from "../../components/chat-box/ChatBox";
import {PDFRenderer} from "../../components/pdf-renderer/PDFRenderer";
import {SideBar} from "../../components/side-bar/SideBar";

export function HomePage(){
    return <div className="homepage">
        <SideBar/>
        <ChatBox/>
        <PDFRenderer/>
    </div>
}