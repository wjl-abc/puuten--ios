//
//  FriendsTableCell.h
//  puuten
//
//  Created by wang jialei on 12-8-14.
//
//

#import <UIKit/UIKit.h>

@interface FriendsTableCell : UITableViewCell
{
    UIImageView *avatar;
    UILabel *nameLbl;
    UIButton *checked;
    BOOL isChecked;
    BOOL justForShow;
}

- (void)setValue:(NSString *)name avatar:(NSString *)image_url justForShow:(BOOL)just_for_show;
@end
