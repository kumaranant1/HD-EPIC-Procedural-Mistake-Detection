You are creating one controlled counterfactual mistake for online procedural mistake detection.

Goal:
prepare Scrambled Eggs with Green Peppers and Mushrooms

High-level recipe steps, for reference only:
- Crack the eggs into a bowl, add salt and pepper and beat.
- Wash the vegetables. Next, slice the mushrooms and chop the bell pepper.
- Heat a pan over medium heat. Once heated, pour 1tbsp of olive oil, spread and add the egg mixture and the vegetables.
- Stir-fry for at least 5 minutes, or until the eggs are cooked as desired.
- Season to taste and serve.

The action stream has 381 actions. The approximate midpoint is action index 190.
Choose exactly one critical action from the candidate actions near this midpoint.

For this task, a critical action means a committed recipe-state change: an action where an ingredient, food item, tool, heat source, cooking vessel, or appliance is used in a way that directly changes the recipe outcome right now. Changing this action should be hard to recover from, not something the person can simply undo in the next moment or reinterpret as a different harmless side task.

Good critical targets usually look like:
- adding, pouring, sprinkling, mixing, stirring, draining, discarding, transferring, or combining ingredients into the actual recipe mixture or cooking vessel
- putting food or liquid into a specific cooking vessel, appliance, oven, pan, pot, fridge, or freezer when that placement directly changes the recipe state
- applying heat, choosing cooking temperature or time, starting a cooking/blending/frothing process after ingredients are committed
- using a tool that directly transforms the food, such as cutting, blending, grinding, straining, or frothing

Noise/support actions are not valid targets. Leave these unchanged:
- opening or closing doors, cupboards, drawers, packets, lids, fridges, or appliance doors
- picking up, putting down, holding, moving, checking, looking at, or arranging objects before they are used
- plugging, unplugging, switching power on/off, pressing generic power buttons, or moving cables
- cleaning, wiping, tidying, drinking water, using a phone, walking, waiting, or repositioning the body/camera
- selecting or picking up an ingredient without adding it to the recipe yet
- staging or holding ingredients in a temporary mug, glass, bowl, plate, or container before they enter the recipe
- pouring something into a separate container if it could plausibly be for another harmless use

Example: replacing "pick up a jar of spices" with "pick up sugar" is not a good mistake, because the person could notice before adding it. Replacing "add the spices into the pan" with "add sugar into the pan" is a good mistake, because the wrong ingredient has been committed to the recipe.
Example: replacing "pour hot water into a mug" with "pour vinegar into a mug" is not a good mistake unless that mug is already the recipe mixture or final food state. The person could be preparing something else, and the bad ingredient has not entered the recipe yet.
Example: replacing "pour milk into the frother" with "pour milk into the mug" is usually not a good mistake, because the milk may still be transferable or the mug may be part of the coffee workflow. Prefer a replacement like adding the wrong ingredient into the frother, adding the milk into an already incompatible mixture, overheating it, contaminating it, or using a directly recipe-breaking quantity.

Previous context before the candidate window (this is the previous partial context). These actions will remain unchanged:

103. Use the back of the knife to crack open the shell of the egg held by the left hand.

104. Put down the knife in the right hand on top of the wooden chopping board below.

105. With both hands, pull apart the eggshells after they have been cracked.

106. Pour the egg yellow as well as the egg white into the box below by shaking the egg shells over the box with both hands.

107. Stack the two eggshells together with both hands.

108. With the left hand, throw away the eggshells into the rubbish bin.

109. Close the lid of the rubbish bin with the pinky finger of the left hand.

110. With the left hand, turn on the tap.

Candidate actions. Choose exactly one target_index from this list:

111. Wash both hands under the running tap water after dealing with the eggs.

112. Turn off the tap with the right hand after washing my hands.

113. Shake both hands over the kitchen sink in order to get rid of excess water on them after washing.

114. With the right hand, pick up the kitchen towel that is hanging by the handle of the drawer below.

115. Use the kitchen towel to wipe both hands to get them dry after washing them.

116. With both hands, grab the lid of the egg carton container and close it.

117. Pick up the egg carton from the wooden chopping board using both hands.

118. Place the egg carton on the counter top that is on the other side next to the weighing scale. We want to put them away as we do not require more eggs in this recipe.

119. Grab the box containing the raw egg and move it a bit further into the wooden chopping board with both hands in order to make some space on the wooden chopping board below.

120. With the right hand, pick up the spoon and lift it from the wooden chopping board on which it was placed.

121. With the right hand, pick up the salt jar from the wooden chopping board while also holding the spoon in the right hand.

122. Hold the salt jar in the left hand and use the right hand to unscrew its lid while also holding a tablespoon.

123. Put down the lid of the salt jar on the wooden chopping board below with the right hand.

124. Use the spoon in the right hand to scoop up some salt from the jar held by the left hand.

125. Add the salt to the plastic box containing the raw egg using the spoon held by the right hand.

126. With the right hand, pick up the lid of the salt jar from the wooden chopping board.

127. Use the right hand to screw back the lid of the salt jar after using it.

128. Put down the salt jar back on the wooden chopping board below with the left hand.

129. With the left hand, pick up the other jar containing ground pepper.

130. With the right hand, open the lid of the pepper jar while holding the pepper jar in the left hand.

131. Hold the jar and the lid with the left hand and use the spoon in the right hand to scoop up some ground pepper from the jar.

132. Add the pepper from the spoon to the container below which contains raw egg.

133. Put some pepper back into the jar that was excess using the spoon in the right hand.

134. Take the lid from the left hand using the right hand.

135. Screw the lid back on top of the pepper jar with the right hand which is also holding a spoon.

136. With the left hand, put down the pepper jar.

137. With both hands, pick up and move the salt jar and the pepper jar to the corner of the chopping board below.

138. Put down the spoon on the wooden chopping board below as we are done adding salt and pepper to the egg mixture.

139. Pick up a pen from the notebook.

140. Open the cap of the marker or pen with both hands.

141. Using the marker in the right hand, write down the ingredient and how much of it was added into the recipe.

142. After writing down information in the notebook close the cap of the marker with both hands.

143. Place the pen back on the notebook with the right hand.

144. Pull up the sleeve of the right hand as it might have been getting in the way of cooking.

145. With the left hand, pick up the bottle of olive oil and lift it from the wooden chopping board below.

146. With the right hand, grab and push in the plastic container containing the egg mixture.

147. Transfer the bottle of olive oil from the left hand to the right hand.

148. Open the door to the cabinet below with the left hand.

149. Place the bottle of olive oil on the lower shelf of the cabinet with the right hand.

150. Close the door to the cabinet below with the left hand.

151. With the right hand, open the door to the refrigerator below.

152. Slightly bend down and look at all the available items in the refrigerator.

153. With the left hand, reach into the refrigerator and grab a whole yellow pepper from the bottom shelf.

154. Examine it and put the yellow pepper back inside the refrigerator with the left hand.

155. With the left hand, pick up a green pepper from the bottom shelf of the refrigerator.

156. Place the green pepper on the countertop with the left hand.

157. With the left hand, reach into the bottom shelf of the refrigerator and take out a small plastic container containing mushrooms.

158. Hold the box of mushroom with both hands and use the left hand to pick up and examine the mushrooms.

159. Place one single mushroom on top of the wooden chopping board with the left hand.

160. With the left hand, place the box of mushrooms back into the lower shelf of the refrigerator as we do not require more mushrooms for this recipe.

161. Transfer the box of mushrooms to the right hand.

162. With the left hand, pull out a piece of plastic that was covering the space on the lower shelf of the refrigerator.

163. With the right hand, place the box of mushrooms on the lower shelf of the refrigerator.

164. Close the door of the refrigerator with the right hand.

165. With the right hand, pick up the green pepper from the countertop.

166. With the left hand, pick up the mushroom from the wooden chopping board while also holding the piece of plastic.

167. Place both the mushroom as well as the green pepper on the wooden chopping board with both hands next to the other ingredients.

168. With the left hand, open the lid to the rubbish bin below.

169. Throw away the piece of plastic held by the right hand into the rubbish bin.

170. Close the lid of the rubbish bin with the left hand.

171. With both hands, grab the mushroom and the green pepper one in each hand.

172. Place the green pepper a bit further away on the wooden chopping board with the right hand.

173. Transfer the mushroom from the left hand to the right hand.

174. Use the left hand to turn on the tap in the kitchen sink.

175. Wash the mushroom in the right hand under the kitchen tap so as to rinse it and to clean any dust that is on the surface of the mushroom.

176. With the left hand, reach and pick up the green pepper from the wooden chopping board so that we can wash it as well.

177. Place the green pepper on the countertop next to the kitchen sink with the left hand.

178. With both hands, wash the mushroom so as to clean and rinse any dirt off of it.

179. With the right hand, shake the mushroom over the kitchen sink in order to get rid of excess water on it after washing.

180. Place the mushroom on the wooden chopping board with the left hand.

181. With the right hand, pick up the green pepper from the counter top next to the kitchen sink so that it can be washed next.

182. Transfer the green pepper to the left hand from the right hand.

183. With the right hand, turn on the tap in the kitchen sink.

184. With both hands, scrub and rinse the green pepper under running water to clean it as well as to get any bacteria or dirt on it to fall into the kitchen sink.

185. After cleaning the green pepper, use the right hand to turn off the tap.

186. Shake the green pepper in the right hand over the kitchen sink in order to get rid of the excess liquid on it after washing.

187. Transfer the green pepper from the right hand to the left hand.

188. With the right hand, pick up the mushroom from the wooden chopping board.

189. Place the green pepper in the left hand on the wooden chopping board below.

190. Place the mushroom on the wooden chopping board below with the right hand next to the green pepper.

191. With the left hand, open the drawer below revealing utensils and other items.

192. With the left hand, push the drawer back in in order to close it.

193. With the left hand, open the other drawer to the left of the previously opened drawer revealing utensils and other items.

194. With the right hand, reach into the back side of the drawer and pull out a plastic white chopping board.

195. Close the drawer with the left hand.

196. Place the chopping board on the wooden chopping board with both hands.

197. Grab the handle of the knife and slightly reposition it with the right hand.

198. With the left hand, pick up the green pepper from the wooden chopping board by grabbing it.

199. Place the green pepper at the center of the white plastic chopping board below with the left hand.

200. Use the knife in the right hand to cut through the green pepper held by the left hand over the white plastic chopping board.

201. After cutting the pepper into two halves, place the half held by the left hand on the wooden chopping board behind the plastic white chopping board.

202. Use the left hand to grab a seed of the pepper that is stuck to the blade of the knife held by the right hand and drop the seed over the plastic white chopping board below.

203. With the left hand, grab and rotate the half of the green pepper that is on the plastic white chopping board

204. With the knife in the right hand, cut out the white core of the green pepper held by the left hand.

205. Put down the knife with the right hand.

206. While holding the pepper in the left hand, use the right hand to grab and remove the core of the green pepper.

207. Open the lid of the rubbish bin with the left hand.

208. Throw away the core of the pepper held in the right hand into the rubbish bin.

209. Close the lid of the rubbish bin with the left hand.

210. With the left hand, grab the green pepper on the plastic chopping board and turn it over on its side.

211. With the right hand, pick up the knife.

212. Cut the green pepper piece into two halves with the knife in the right hand.

213. Pick up and place the piece of green pepper in the left hand on the wooden chopping board.

214. With the left hand, pick up and move the seeds fallen onto the plastic white chopping board.

215. Using the knife in the right hand, cut the green pepper further into two halves.

216. Using the knife, further cut the green pepper into thin slices.

217. Pick the green pepper piece stuck to the knife blade with the left hand and put it on the chopping board below.

218. Rotate the green pepper slices onto their sides with the left hand.

219. Using the knife in the right hand, cut the slices of green pepper into tiny pieces.

220. With the left hand, slide over the blade of the knife in order to get the bits of pepper stuck to it to fall back on the plastic white chopping board below.

221. With the left hand, push the pieces of green pepper into a neat pile at the center of the plastic chopping board.

222. With the left hand, pick up the other large piece of green pepper from the wooden chopping board and place it on the plastic chopping board below.

223. With the knife in the right hand, cut the green pepper piece into thin slices.

224. Place the large piece of green pepper back on the wooden chopping board with the left hand.

225. Hold the small slice of green pepper in the left hand and cut it into small bits with the knife in the right hand.

226. Push the small pieces of green pepper into the pile with the left hand.

227. Put down the knife that is in the right hand on top of the wooden chopping board below.

228. With the left hand, pick up the mushroom from the wooden chopping board.

229. Place the mushroom onto the plastic white chopping board below with the left hand.

230. Cut the mushroom into two equal halves using the knife in the right hand.

231. Put away half of the mushroom back on the wooden chopping board with the right hand.

232. Cut the half of the mushroom on the plastic chopping board into thin slices with the knife in the right hand.

233. Rotate the mushroom onto its side with the left hand.

234. Continue chopping the mushroom half into thin slices using the knife in the right hand.

235. Rotate the mushroom towards the side with the left hand.

236. Continue chopping the mushroom into even more thin pieces using the knife in the right hand.

237. Push the pile of finely chopped mushroom pieces next to the pile of finely chopped green pepper pieces on the chopping board with the left hand.

238. Put down the knife on the wooden chopping board below with the right hand.

239. With the right hand, push away the green pepper pieces in order to clear them on the wooden chopping board.

240. With the left hand, open the door to the cabinet above revealing serving bowls and other crockery.

241. With the right hand, grab a serving bowl from the stack of other serving bowls from the lower shelf of the cabinet.

242. Close the door to the cabinet with the left hand.

243. With the right index finger, press the power button of the weighing scale several times in order to turn it on.

244. Place the bowl in the right hand over the weighing scale in order to use it as a base to weigh other ingredients so that we do not directly use the surface of the weighing scale as it will get dirty.

245. Press the buttons of the weighing scale with both hands in order to configure it correctly.

246. With the left index finger, press the power button to turn off the weighing scale.

247. With the left index finger, press the power button to turn the weighing scale back on.

248. With the left hand, slide and pick up the plastic white chopping board that contains finely chopped vegetables.

249. With the right hand, pick up the knife from the wooden chopping board below.

250. Transfer the finely chopped green pepper pieces from the plastic chopping board to the bowl over the weighing scale in order to measure the weight of the green pepper pieces.

251. Place the plastic white chopping board as well as the knife on top of the wooden chopping board.

252. With the right hand, pick up the marker that is lying on the notebook.

253. With both hands, open the cap of the marker.

254. With the marker in the right hand note down the name of the ingredient and its weight.

255. Put down the marker back on the notebook using the right hand.

256. With the left hand, press the power button of the weighing scale in order to turn it off.

257. With the left hand, press the power button of the weighing scale in order to turn it back on.

258. With the left and the right hand, pick up the plastic white chopping board containing the mushroom pieces as well as the knife in the right hand.

259. With the knife in the right hand, push and transfer the finely chopped mushroom pieces from the chopping board onto the bowl below, which is placed over the weighing scale. With this we can measure the weight of the mushroom pieces.

260. Place the plastic chopping board as well as the knife on top of the wooden chopping board with both hands.

261. With the left hand, pick up the mushroom pieces that have been lumped together and break them apart in the serving bowl over the weighing scale.

262. Pick up the marker on the notebook with the right hand.

263. With the marker in the right hand, write down the name of the ingredient and its measured weight.

264. Put down the marker over the notebook with the right hand.

265. With the left thumb, press the power button of the weighing scale in order to turn it off.

266. Pick up the bowl containing the chopped vegetables from the weighing scale with the left hand.

267. Place the bowl containing chopped vegetables on the wooden chopping board with the left hand.

268. With the right hand, pick up and move the position of the knife over the wooden chopping board.

269. With the left hand, pick up and slide the plastic white chopping board on the wooden chopping board in order to arrange it nicely.

Future reference actions from the original stream (this is the future partial context). These will be removed after the changed action; use them only to understand what the procedure was trying to accomplish:

270. With the left hand, grab the handlebar of the cabinet towards the left and slightly open it and close it back as we decided not to open it.

271. With the right hand, grab the right door's handle, which is the refrigerator's door, and open it.

272. Reach into the refrigerator with the left hand and grab a pile of plastic boxes from the upper shelf of the refrigerator.

273. Transfer the pile of boxes from the left hand to the right hand.

274. With the left hand, reach into the refrigerator again and pull out another plastic container from the upper shelf of the refrigerator.

275. Place the box in the right hand back into the upper shelf of the refrigerator.

276. Accidentally drop a box onto the ground below with both hands.

277. With the right hand, reach down and pick up the plastic container that had fallen to the ground.

Task:

1. Select the most suitable critical action from candidate_action_indices: [111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269].

2. Replace only that action with one plausible action-level mistake.

3. Do not insert actions. Do not delete actions before the selected target.

4. If many candidate actions are noise/support actions, ignore them and choose the best committed recipe-state action that remains in the candidate list.

Rules:
- The replacement must be a natural HD-EPIC-style action narration, not an explanation.
- The replacement must be plausible given the previous context.
- The replacement must break or seriously threaten the goal.
- Do not choose actions from parallel side tasks, even if they involve food, ingredients, bowls, mugs, or utensils. A candidate action is valid only if it directly advances the stated goal or one of the recipe steps.
- If an action prepares or modifies another food/drink not mentioned in the goal or recipe steps, treat it as natural noise. Leave it unchanged.
- The mistake must be observable as goal-breaking at this action, not only after assuming a later future action.
- Prefer mistakes that commit the wrong ingredient/tool/quantity/order/temperature/contamination into the recipe state.
- The mistake should be hard to recover from without restarting, discarding food, removing mixed ingredients, or substantially redoing the procedure.
- Do not choose reversible setup/support actions such as picking something up, opening/closing, plugging/unplugging, switching power, or pressing generic power buttons.
- Do not create mistakes that only move the correct ingredient into a different clean temporary container.
- Do not create mistakes whose only problem is "this might be used wrongly later."
- The replacement must not be a harmless variation, preference, or common valid alternative.
- The replacement must not be a wild or cartoonish failure. It should look like a realistic human procedural slip: wrong ingredient added, wrong tool used on food, wrong cooking medium, wrong amount, wrong temperature, wrong time, wrong order after a commitment point, or contamination.
- The replacement must not be trivially detectable from wording alone. Avoid words like "mistake", "wrongly", "accidentally", "fails", or "error" in the action text.
- Do not use cartoonish failures such as dropping everything, leaving the kitchen, destroying equipment, unplugging everything, or doing nothing.
- Do not modify the recipe steps. leave them as they are, even if they no longer match the changed action.
- Do not add any second mistake.
- After this one replacement in the candidate actions, the stream will be truncated, so do not describe recovery or later correction.

Rationale fields:
- why_this_action_is_critical: explain why the selected original action directly controls the recipe outcome, not just scene setup.
- why_goal_breaking: explain how the replacement prevents or seriously damages the stated goal.
- why_observable_now: explain why the replacement is already a mistake at this action, without relying on an assumed later action.
- why_hard_to_recover: explain why the changed recipe state cannot be easily undone by the next action.
- why_plausible: explain why a real person could plausibly make this slip in the given context.

(Example response format) Return JSON only, with this exact schema:
{
  "target_index": 190,
  "original_action_text": "",
  "mistake_action_text": "",
  "mistake_type": "wrong_ingredient",
  "why_this_action_is_critical": "",
  "why_goal_breaking": "",
  "why_observable_now": "",
  "why_hard_to_recover": "",
  "why_plausible": "",
  "detectability": "subtle",
  "confidence": "high"
}

Schema constraints:
- target_index must be one of: [111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269].
- original_action_text must exactly match the selected candidate action text.
- mistake_type must be one of: wrong_ingredient, wrong_tool, wrong_quantity, wrong_order, wrong_temperature, wrong_temperature_time, contamination, other.
- Use wrong_ingredient only when the ingredient is actually added, poured, mixed, sprinkled, or otherwise committed to the food.
- Use wrong_tool only when the tool directly transforms or contacts the food.
- Use wrong_temperature for incorrect heat level, appliance mode, or temperature setting.
- Use wrong_temperature_time for incorrect cooking/heating/chilling duration.
- detectability must be "subtle" or "moderate"; avoid obvious mistakes.
- confidence must be "high", "medium", or "low".
