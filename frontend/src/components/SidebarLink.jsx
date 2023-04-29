
function SidebarLink({ Icon, text, active }) {
  return (
    <div className="rounded-full text-xl p-4 flex text-slate-200 hover:bg-blue-300 hover:bg-opacity-10 cursor-pointer">
      {Icon}
      {/* <Icon className="h-7" /> */}
      <span className="hidden md:inline lg:inline xl:inline ml-2">{text}</span>
    </div>
  );
}

export default SidebarLink;