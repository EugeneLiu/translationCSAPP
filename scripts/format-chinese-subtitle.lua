-- Automation 4 demo script
-- use blank split Chinese character and English character or number character

script_name = "格式化中文字幕"
script_description = "依照中文排版指北将中文字符和英文字符或者数字使用空格隔开"
script_author = "Eugene Liu"
script_version = "1.0.0"

re = require 'aegisub.re'

function format_chinese_line(line)
	if line.style == 'Chinese' then
		local out_str, rep_count 
		out_str, rep_count = re.sub(line.text, "([\\u2000-\\u206F\\u3000-\\u303F\\u4E00-\\u9FBF\\uFF00-\\uFFEF^\\.^\\s]+)", " \\1 ")
		line.text = out_str
		return line
	else
		return line
	end
end

function format_chinese_subtitle(subtitles, selected_lines, active_line)
	config = {
		{class="label", label="请使用 Chinese 作为中文字幕的样式名", x=0, y=0}
	}
	btn, result = aegisub.dialog.display(config,
	    {"当前选中中文字幕", "全部中文字幕"},
	    {select="当前选中中文字幕", all="全部中文字幕"})

	if btn == "当前选中中文字幕" then
		for z, i in ipairs(selected_lines) do
			local line = subtitles[i]
			subtitles[i] = format_chinese_line(line)
		end
	elseif btn == "全部中文字幕" then
		for i=1, #subtitles do
			local line = subtitles[i]
			subtitles[i] = format_chinese_line(subtitles[i])
		end
	else
	end
	aegisub.set_undo_point(script_name)
end

aegisub.register_macro(script_name, script_description, format_chinese_subtitle)